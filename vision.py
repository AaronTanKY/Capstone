import cv2
import numpy as np
from pybear import Manager
import time

# --- CONFIGURATION ---
M_IDS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
HEAD_PAN_ID = 1
HEAD_TILT_ID = 2
TAG_SIZE = 0.05  # 5cm
# Standard camera matrix for 720p (Replace with real calibration for precision)
K = np.array([[900, 0, 640], [0, 900, 360], [0, 0, 1]], dtype=np.float32)
D = np.zeros((5, 1)) # No distortion assumed

# Simple vision-to-joint mapping gains. Tune these on your hardware.
TARGET_X = 0.0
TARGET_Y = 0.0
X_GAIN = 0.9
Y_GAIN = 0.9
X_DEADBAND = 0.01
Y_DEADBAND = 0.01
MAX_DELTA_PER_STEP = 0.03
CONTROL_HZ = 20.0

# Setup ArUco for AprilTag 36h11
# Note: In older OpenCV, use cv2.aruco.DICT_APRILTAG_36h11
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_APRILTAG_36H11)
parameters = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)


def _apply_deadband(value, deadband):
    if abs(value) < deadband:
        return 0.0
    return value


def _compute_head_goals(current_pan, current_tilt, tx, ty):
    """
    Convert tag translation error to head pan/tilt goals.
    """
    x_error = _apply_deadband(tx - TARGET_X, X_DEADBAND)
    y_error = _apply_deadband(ty - TARGET_Y, Y_DEADBAND)

    pan_delta = float(np.clip(-X_GAIN * x_error, -MAX_DELTA_PER_STEP, MAX_DELTA_PER_STEP))
    tilt_delta = float(np.clip(-Y_GAIN * y_error, -MAX_DELTA_PER_STEP, MAX_DELTA_PER_STEP))

    return current_pan + pan_delta, current_tilt + tilt_delta

def main():
    cap = cv2.VideoCapture(0)
    last_control_time = 0.0
    
    # Initialize BEAR
    try:
        bear = Manager.BEAR(port='COM3', baudrate=8000000)
        bear.set_torque_enable(*[(m_id, 1) for m_id in M_IDS])
    except:
        print("Robot not found, running in Vision-Only mode.")
        bear = None

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # 1. Detect
            corners, ids, _ = detector.detectMarkers(gray)

            if ids is not None:
                # 2. Estimate Pose (returns Rotation and Translation)
                # This replaces the need for the pupil-apriltags library
                obj_points = np.array([
                    [-TAG_SIZE/2,  TAG_SIZE/2, 0],
                    [ TAG_SIZE/2,  TAG_SIZE/2, 0],
                    [ TAG_SIZE/2, -TAG_SIZE/2, 0],
                    [-TAG_SIZE/2, -TAG_SIZE/2, 0]
                ], dtype=np.float32)

                for i in range(len(ids)):
                    _, rvec, tvec = cv2.solvePnP(obj_points, corners[i], K, D)
                    
                    # Translation vector (tx, ty, tz)
                    tx, ty, _ = tvec.flatten()
                    
                    tag_id = int(ids[i][0])
                    print(f"Tag {tag_id}: X={tx:.2f} Y={ty:.2f}")

                    # 3. Motor Commands (Apply gains here as before)
                    if bear and i == 0:
                        now = time.time()
                        if now - last_control_time >= (1.0 / CONTROL_HZ):
                            try:
                                head_ids = [HEAD_PAN_ID, HEAD_TILT_ID]
                                bulk_result = bear.bulk_read(head_ids, ['present_position'])
                                current_pan = bulk_result[0][0][0]
                                current_tilt = bulk_result[1][0][0]

                                goal_pan, goal_tilt = _compute_head_goals(current_pan, current_tilt, tx, ty)

                                bear.bulk_write(head_ids, ['goal_position'], [[goal_pan], [goal_tilt]])
                                last_control_time = now
                            except Exception as exc:
                                print(f"BEAR control error: {exc}")

                    # Visual Feedback
                    cv2.drawFrameAxes(frame, K, D, rvec, tvec, 0.1)
                    cv2.aruco.drawDetectedMarkers(frame, corners)

            cv2.imshow("Windows-Friendly AprilTag", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except KeyboardInterrupt:
        print("Interrupted by user. Disabling BEAR torque...")
        if bear:
            try:
                bear.set_torque_enable(*[(m_id, 0) for m_id in M_IDS])
            except Exception:
                pass
    except Exception as exc:
        print(f"Vision loop error: {exc}")
        if bear:
            try:
                bear.set_torque_enable(*[(m_id, 0) for m_id in M_IDS])
            except Exception:
                pass
    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

