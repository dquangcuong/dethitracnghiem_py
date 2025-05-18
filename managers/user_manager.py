import json
import os

USERS_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'users.json')

def load_users():
    """Đọc danh sách users từ file JSON"""
    try:
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

def save_users(users):
    """Lưu danh sách users vào file JSON"""
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=2, ensure_ascii=False)

def change_password(username, old_password, new_password):
    """
    Đổi mật khẩu cho user
    Trả về True nếu đổi thành công, False nếu thất bại (username hoặc old_password sai)
    """
    users = load_users()
    for user in users:
        if user.get('username') == username and user.get('password') == old_password:
            user['password'] = new_password
            save_users(users)
            return True
    return False
