from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import oracledb

oracledb.init_oracle_client(
    lib_dir=r"C:\Users\Lito\Downloads\instantclient-basic-windows.x64-23.26.1.0.0\instantclient_23_26"
)

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "oracle+oracledb://dotado:202400926@localhost:1521/?service_name=XE"
app.config["SECRET_KEY"] = "secret"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route("/")
def home():
    return "Backend running!"

# ================= AUTH ================= #

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

    hashed_pw = bcrypt.generate_password_hash(data.get("password")).decode("utf-8")

    try:
        db.session.execute(db.text("""
            INSERT INTO USERS (id, name, email, password_hash,
                student_id_number, course, year_level, department)
            VALUES (users_seq.NEXTVAL, :name, :email, :pw,
                :student_id, :course, :year, :dept)
        """), {
            "name": data.get("name"), "email": email, "pw": hashed_pw,
            "student_id": student_id, "course": data.get("course"),
            "year": data.get("year_level"), "dept": data.get("department")
        })
        db.session.commit()
        return jsonify({"message": "Registered successfully"}), 201
    except Exception as e:
        db.session.rollback()
        print("REGISTER ERROR:", e)
        return jsonify({"message": "Server error"}), 500


@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    res = db.session.execute(
        db.text("""
            SELECT id, name, email, password_hash,
                   student_id_number, course, year_level, department
            FROM USERS WHERE email = :email
        """),
        {"email": data.get("email")}
    ).fetchone()

    if not res:
        return jsonify({"message": "User not found"}), 404

    if bcrypt.check_password_hash(str(res[3]), data.get("password")):
        return jsonify({
            "user_id": res[0], "name": res[1], "email": res[2],
            "student_id_number": res[4], "course": res[5],
            "year_level": res[6], "department": res[7]
        })

    return jsonify({"message": "Invalid password"}), 401


# ================= PRODUCTS ================= #

@app.route("/api/products", methods=["GET"])
def get_products():
    try:
        result = db.session.execute(db.text("""
            SELECT id, title, description, price, category, status, seller_id
            FROM PRODUCTS
            WHERE status = 'Available'
            ORDER BY id DESC
        """))
        products = []
        for row in result:
            products.append({
                "id": row[0], "title": row[1], "description": row[2],
                "price": float(row[3]), "category": row[4], "status": row[5],
                "seller_id": row[6], "image_url": None
            })
        return jsonify(products)
    except Exception as e:
        print("GET PRODUCTS ERROR:", e)
        return jsonify({"message": "Server error"}), 500


@app.route("/api/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    try:
        res = db.session.execute(db.text("""
            SELECT p.id, p.title, p.description, p.price, p.category,
                   p.status, p.pickup_location, p.created_at,
                   u.name AS seller_name, p.seller_id
            FROM PRODUCTS p
            LEFT JOIN USERS u ON p.seller_id = u.id
            WHERE p.id = :id
        """), {"id": product_id}).fetchone()

        if not res:
            return jsonify({"message": "Product not found"}), 404

        return jsonify({
            "id": res[0], "title": res[1], "description": res[2],
            "price": float(res[3]), "category": res[4], "status": res[5],
            "pickup_location": res[6],
            "created_at": str(res[7]) if res[7] else None,
            "seller_name": res[8], "seller_id": res[9],
            "image_url": None
        })
    except Exception as e:
        print("GET PRODUCT ERROR:", e)
        return jsonify({"message": "Server error"}), 500


@app.route("/api/products", methods=["POST"])
def create_product():
    data = request.get_json()
    try:
        db.session.execute(db.text("""
            INSERT INTO PRODUCTS (id, title, description, price,
                category, pickup_location, seller_id, created_at, status)
            VALUES (products_seq.NEXTVAL, :title, :description, :price,
                :category, :pickup_location, :seller_id, SYSDATE, 'Available')
        """), {
            "title": data.get("title"), "description": data.get("description"),
            "price": data.get("price"), "category": data.get("category", "General"),
            "pickup_location": data.get("pickup_location", "N/A"),
            "seller_id": data.get("user_id")
        })
        db.session.commit()
        return jsonify({"message": "Product created successfully"}), 201
    except Exception as e:
        db.session.rollback()
        print("PRODUCT ERROR:", e)
        return jsonify({"message": "Server error"}), 500


# ✅ EDIT product
@app.route("/api/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    data = request.get_json()
    user_id = data.get("user_id")
    try:
        # verify ownership
        owner = db.session.execute(
            db.text("SELECT seller_id FROM PRODUCTS WHERE id = :id"),
            {"id": product_id}
        ).scalar()

        if not owner or int(owner) != int(user_id):
            return jsonify({"message": "Unauthorized"}), 403

        db.session.execute(db.text("""
            UPDATE PRODUCTS SET
                title = :title,
                description = :description,
                price = :price,
                category = :category
            WHERE id = :id
        """), {
            "title": data.get("title"),
            "description": data.get("description"),
            "price": data.get("price"),
            "category": data.get("category"),
            "id": product_id
        })
        db.session.commit()
        return jsonify({"message": "Product updated successfully"})
    except Exception as e:
        db.session.rollback()
        print("UPDATE PRODUCT ERROR:", e)
        return jsonify({"message": "Server error"}), 500


# ✅ DELETE product
@app.route("/api/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    user_id = request.args.get("user_id")
    try:
        # verify ownership
        owner = db.session.execute(
            db.text("SELECT seller_id FROM PRODUCTS WHERE id = :id"),
            {"id": product_id}
        ).scalar()

        if not owner or int(owner) != int(user_id):
            return jsonify({"message": "Unauthorized"}), 403

        db.session.execute(
            db.text("DELETE FROM PRODUCTS WHERE id = :id"),
            {"id": product_id}
        )
        db.session.commit()
        return jsonify({"message": "Product deleted successfully"})
    except Exception as e:
        db.session.rollback()
        print("DELETE PRODUCT ERROR:", e)
        return jsonify({"message": "Server error"}), 500


# ================= CART ================= #

@app.route("/api/cart", methods=["GET"])
def get_cart():
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"message": "user_id required"}), 400
    try:
        result = db.session.execute(db.text("""
            SELECT c.id, p.id, p.title, p.price, p.category, p.status
            FROM CART c
            JOIN PRODUCTS p ON c.product_id = p.id
            WHERE c.user_id = :user_id
        """), {"user_id": user_id})

        items = []
        for row in result:
            items.append({
                "cart_id": row[0], "id": row[1], "title": row[2],
                "price": float(row[3]), "category": row[4],
                "status": row[5], "image_url": None
            })
        return jsonify(items)
    except Exception as e:
        print("GET CART ERROR:", e)
        return jsonify({"message": "Server error"}), 500


@app.route("/api/cart", methods=["POST"])
def add_to_cart():
    data = request.get_json()
    try:
        existing = db.session.execute(db.text("""
            SELECT COUNT(*) FROM CART
            WHERE user_id = :user_id AND product_id = :product_id
        """), {"user_id": data.get("user_id"), "product_id": data.get("product_id")}).scalar()

        if existing > 0:
            return jsonify({"message": "Already in cart"}), 400

        db.session.execute(db.text("""
            INSERT INTO CART (id, user_id, product_id, added_at)
            VALUES (cart_seq.NEXTVAL, :user_id, :product_id, SYSDATE)
        """), {"user_id": data.get("user_id"), "product_id": data.get("product_id")})
        db.session.commit()
        return jsonify({"message": "Added to cart"}), 201
    except Exception as e:
        db.session.rollback()
        print("ADD CART ERROR:", e)
        return jsonify({"message": "Server error"}), 500


@app.route("/api/cart/<int:cart_id>", methods=["DELETE"])
def remove_from_cart(cart_id):
    try:
        db.session.execute(
            db.text("DELETE FROM CART WHERE id = :id"),
            {"id": cart_id}
        )
        db.session.commit()
        return jsonify({"message": "Removed from cart"})
    except Exception as e:
        db.session.rollback()
        print("REMOVE CART ERROR:", e)
        return jsonify({"message": "Server error"}), 500


# ================= CHECKOUT ================= #

@app.route("/api/checkout", methods=["POST"])
def checkout():
    data = request.get_json()
    try:
        db.session.execute(db.text("""
            DELETE FROM CART WHERE user_id = :user_id
        """), {"user_id": data.get("user_id")})
        db.session.commit()
        return jsonify({"message": "Order placed successfully"})
    except Exception as e:
        db.session.rollback()
        print("CHECKOUT ERROR:", e)
        return jsonify({"message": "Server error"}), 500

# ================= MESSAGES ================= #

@app.route("/api/messages", methods=["POST"])
def send_message():
    data = request.get_json()

    try:
        db.session.execute(db.text("""
            INSERT INTO MESSAGES (
                id, sender_id, receiver_id, message_text, sent_at
            )
            VALUES (
                messages_seq.NEXTVAL,
                :sender,
                :receiver,
                :message,
                SYSDATE
            )
        """), {
            "sender": data.get("sender_id"),
            "receiver": data.get("receiver_id"),
            "message": data.get("message_text")
        })

        db.session.commit()
        return jsonify({"message": "Message sent"}), 201

    except Exception as e:
        db.session.rollback()
        print("MESSAGE ERROR:", e)
        return jsonify({"message": "Server error"}), 500


@app.route("/api/messages", methods=["GET"])
def get_messages():
    sender = request.args.get("sender_id")
    receiver = request.args.get("receiver_id")

    try:
        result = db.session.execute(db.text("""
            SELECT sender_id, receiver_id, message_text, sent_at
            FROM MESSAGES
            WHERE 
                (sender_id = :sender AND receiver_id = :receiver)
                OR
                (sender_id = :receiver AND receiver_id = :sender)
            ORDER BY sent_at ASC
        """), {
            "sender": sender,
            "receiver": receiver
        })

        messages = []
        for row in result:
            messages.append({
                "sender_id": row[0],
                "receiver_id": row[1],
                "message_text": row[2],
                "sent_at": str(row[3])
            })

        return jsonify(messages)

    except Exception as e:
        print("GET MESSAGES ERROR:", e)
        return jsonify({"message": "Server error"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)