from flask import Flask, jsonify, request
from datetime import datetime
import re

app = Flask(__name__)

sessions = []
next_session_id = 1

TIME_FMT = "%Y-%m-%dT%H:%M:%S"
NAME_RE = re.compile(r'^[A-Za-z0-9_-]{3,20}$')



def validate_task_name(task_name: str):
    if not isinstance(task_name, str):
        return False
    pattern = r"^[A-Za-z0-9_-]{3,20}$"
    return re.fullmatch(pattern, task_name) is not None

def find_session(session_id):
    for s in sessions:
        if s["session_id"] == session_id:
            return s
    return None

def serialize_helper(session):
    started_at = session["started_at"]
    stopped_at = session["stopped_at"]
    if stopped_at is not None and session["duration_seconds"] is not None:
        duration_seconds = session["duration_seconds"]
    else:
        now = datetime.now()
        duration_seconds = int((now - started_at).total_seconds())
    return {
        "session_id": session["session_id"],
        "task_name": session["task_name"],
        "started_at": started_at.isoformat(timespec="seconds"),
        "stopped_at": stopped_at.isoformat(timespec="seconds") if stopped_at else None,
        "duration_seconds": duration_seconds,
        "status": session["status"],
    }
# from flask import send_from_directory

# @app.route("/")
# def home():
#     return send_from_directory("static", "index.html")

@app.route("/sessions/start", methods=["POST"])
def start_session():
    global next_session_id
    data = request.get_json(silent=True) or {}
    task_name = data.get("task_name")
    if not validate_task_name(task_name):
        return (
            jsonify(
                {"error": "Invalid task name", "message": "Task name must be between 3 and 20 characters"}
            ), 400
        )
    start_at = datetime.now()
    session = {
        "session_id": next_session_id,
        "task_name": task_name,
        "started_at": start_at,
        "stopped_at": None,
        "duration_seconds": None,
        "status": "running"
    }
    sessions.append(session)
    next_session_id += 1
    
    return jsonify(serialize_helper(session)), 201

@app.route("/sessions/<int:session_id>/stop", methods=["POST"])
def stop_session(session_id):
    session = find_session(session_id)
    if session is None:
        return (jsonify({"error": "Session not found", "message": f"No session with ID {session_id}"}), 404,)

    if session["status"] == "completed":
        return (jsonify({"error": "Session already stopped", "message": f"Session {session_id} was already stopped"}),
            400,
        )
    stopped_at = datetime.now()
    duration = (stopped_at - session["started_at"]).total_seconds()
    session["stopped_at"] = stopped_at
    session["duration_seconds"] = int(duration)
    session["status"] = "completed"

    return jsonify(serialize_helper(session)), 200

@app.route("/sessions", methods=["GET"])
def list_sessions():
    status = request.args.get("status")
    if status and status not in ("running", "completed"):
        return (jsonify({"error": "Invalid Status", "message": f"Status must be binary"}), 400)

    if status:
        filtered = [s for s in sessions if s["status"] == status]
    else:
        filtered = sessions
        
    serialized = [serialize_helper(s) for s in filtered]
    return jsonify({"sessions":serialized, "total": len(serialized)}), 200

@app.route("/sessions/<int:session_id>", methods=["GET"])
def get_session(session_id):
    session = find_session(session_id)
    if session is None:
        return (jsonify({"error": "Session not found", "message": f"No session with ID {session_id}"}), 404,)
    return jsonify(serialize_helper(session)), 200

@app.route("/sessions/<int:session_id>", methods=["DELETE"])
def delete_session(session_id):
    for i, s in enumerate(sessions):
        if s["session_id"] == session_id:
            deleted = sessions.pop(i)
            return (jsonify({"message": "Session deleted successfully", "session_id": deleted["session_id"], "task_name": deleted["task_name"],}), 200)
    return (jsonify({"error": "Session not found","message": f"No session with ID {session_id}"}),404)


if __name__ == "__main__":
    app.run(debug=False)
