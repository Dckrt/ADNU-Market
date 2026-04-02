print("ROUTES LOADED 🔥")

from flask import request, jsonify
from app import app, db, bcrypt
import os

# 🔥 DETECT MODE
IS_RENDER = os.getenv("RENDER")

# ---------------- AUTH ---------------- #

@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json()

    email = data.get("email", "")
    student_id = data.get("student_id_number", "")

    if not email.endswith("@gbox.adnu.edu.ph"):
        return jsonify({"message": "Use ADNU GBOX email only"}), 400

    if "-" not in student_id:
        return jsonify({"message": "Student ID must contain '-'"}), 400

    existing = db.session.execute(
        db.text("SELECT COUNT(*) FROM USERS WHERE email = :email"),
        {"email": email}
    ).scalar()

    if existing > 0:
        return jsonify({"message": "Email already registered"}), 400

    hashed_pw = bcrypt.generate_password_hash(
        data.get("password")
    ).decode("utf-8")

    try:
        # 🔥 DIFFERENT INSERT FOR SQLITE vs ORACLE
        if IS_RENDER:
            # ✅ SQLITE (no sequence)
            db.session.execute(db.text("""
                INSERT INTO USERS (
                    name, email, password_hash,
                    student_id_number, course, year_level, department
                )
                VALUES (
                    :name, :email, :pw,
                    :student_id, :course, :year, :dept
                )
            """), {
                "name": data.get("name") or "Unknown",
                "email": email,
                "pw": hashed_pw,
                "student_id": student_id,
                "course": data.get("course") or "N/A",
                "year": data.get("year_level") or "N/A",
                "dept": data.get("department") or "N/A"
            })
        else:
            # ✅ ORACLE (with sequence)
            db.session.execute(db.text("""
                INSERT INTO USERS (
                    id, name, email, password_hash,
                    student_id_number, course, year_level, department
                )
                VALUES (
                    users_seq.NEXTVAL,
                    :name,
                    :email,
                    :pw,
                    :student_id,
                    :course,
                    :year,
                    :dept
                )
            """), {
                "name": data.get("name") or "Unknown",
                "email": email,
                "pw": hashed_pw,
                "student_id": student_id,
                "course": data.get("course") or "N/A",
                "year": data.get("year_level") or "N/A",
                "dept": data.get("department") or "N/A"
            })

        db.session.commit()
        return jsonify({"message": "Registered successfully"}), 201

    except Exception as e:
        db.session.rollback()
        print("REGISTER ERROR:", e)
        return jsonify({"message": "Server error during registration"}), 500


@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()

    res = db.session.execute(
        db.text("""
            SELECT id, name, email, password_hash,
                   student_id_number, course, year_level, department
            FROM USERS
            WHERE email = :email
        """),
        {"email": data.get("email")}
    ).fetchone()

    if not res:
        return jsonify({"message": "User not found"}), 404

    # 🔥 SAFE PASSWORD CHECK
    if bcrypt.check_password_hash(str(res[3]), data.get("password")):
        return jsonify({
            "user_id": res[0],
            "name": res[1],
            "email": res[2],
            "student_id_number": res[4],
            "course": res[5],
            "year_level": res[6],
            "department": res[7]
        })

    return jsonify({"message": "Invalid password"}), 401


# ---------------- PRODUCTS ---------------- #

@app.route("/api/products", methods=["GET"])
def get_products():
    result = db.session.execute(db.text("""
        SELECT id, title, description, price, category, status
        FROM PRODUCTS
        WHERE status = 'Available'
        ORDER BY id DESC
    """))

    products = []

    for row in result:
        products.append({
            "id": row[0],
            "title": row[1],
            "description": row[2],
            "price": float(row[3]),
            "category": row[4],
            "status": row[5]
        })

    return jsonify(products)


@app.route("/api/products", methods=["POST"])
def create_product():
    data = request.get_json()

    try:
        if IS_RENDER:
            # ✅ SQLITE
            db.session.execute(db.text("""
                INSERT INTO PRODUCTS (
                    title, description, price,
                    category, pickup_location, seller_id, status
                )
                VALUES (
                    :title, :description, :price,
                    :category, :pickup_location, :seller_id, 'Available'
                )
            """), {
                "title": data.get("title"),
                "description": data.get("description"),
                "price": data.get("price"),
                "category": data.get("category", "General"),
                "pickup_location": data.get("pickup_location", "N/A"),
                "seller_id": data.get("user_id")
            })
        else:
            # ✅ ORACLE
            db.session.execute(db.text("""
                INSERT INTO PRODUCTS (
                    id, title, description, price,
                    category, pickup_location, seller_id, created_at, status
                )
                VALUES (
                    products_seq.NEXTVAL,
                    :title,
                    :description,
                    :price,
                    :category,
                    :pickup_location,
                    :seller_id,
                    SYSDATE,
                    'Available'
                )
            """), {
                "title": data.get("title"),
                "description": data.get("description"),
                "price": data.get("price"),
                "category": data.get("category", "General"),
                "pickup_location": data.get("pickup_location", "N/A"),
                "seller_id": data.get("user_id")
            })

        db.session.commit()
        return jsonify({"message": "Product created successfully"}), 201

    except Exception as e:
        db.session.rollback()
        print("PRODUCT ERROR:", e)
        return jsonify({"message": "Server error creating product"}), 500