import datetime

from flask import Blueprint
from flask import render_template, request, redirect, url_for, jsonify
from flask import g

from . import db

bp = Blueprint("pets", "pets", url_prefix="")

def format_date(d):
    if d:
        d = datetime.datetime.strptime(d, '%Y-%m-%d')
        v = d.strftime("%a - %b %d, %Y")
        return v
    else:
        return None
def pets_order_by(cursor,oby,order):
    if oby == "id":
        if order == "asc":
            cursor.execute(f"select p.id, p.name, p.bought, p.sold, s.name from pet p, animal s where p.species = s.id order by p.id")
        else:
            cursor.execute(f"select p.id, p.name, p.bought, p.sold, s.name from pet p, animal s where p.species = s.id order by p.id desc")
    elif oby == "name":
        if order == "asc":
            cursor.execute(f"select p.id, p.name, p.bought, p.sold, s.name from pet p, animal s where p.species = s.id order by p.name")
        else:
            cursor.execute(f"select p.id, p.name, p.bought, p.sold, s.name from pet p, animal s where p.species = s.id order by p.name desc")
    elif oby == "bought":
        if order == "asc":
            cursor.execute(f"select p.id, p.name, p.bought, p.sold, s.name from pet p, animal s where p.species = s.id order by p.bought")
        else:
            cursor.execute(f"select p.id, p.name, p.bought, p.sold, s.name from pet p, animal s where p.species = s.id order by p.bought desc")
    elif oby == "sold":
        if order == "asc":
            cursor.execute(f"select p.id, p.name, p.bought, p.sold, s.name from pet p, animal s where p.species = s.id order by p.sold")
        else:
            cursor.execute(f"select p.id, p.name, p.bought, p.sold, s.name from pet p, animal s where p.species = s.id order by p.sold desc")
    elif oby == "species":
        if order == "asc":
            cursor.execute(f"select p.id, p.name, p.bought, p.sold, s.name from pet p, animal s where p.species = s.id order by p.species")
        else:
            cursor.execute(f"select p.id, p.name, p.bought, p.sold, s.name from pet p, animal s where p.species = s.id order by p.species desc")

    pets = cursor.fetchall()
    return pets
def pets_filter_by(cursor,oby,order,field,value):
    if oby == "id":
        if order == "asc":
            cursor.execute("select p.id, p.name, p.bought, p.sold, s.name from pet p, animal s ,tag tg, tags_pets tg_p where p.id = tg_p.pet AND tg.id = tg_p.tag AND tg.name = ? AND p.species = s.id order by p.id",[value])
        else:
            cursor.execute("select p.id, p.name, p.bought, p.sold, from pet p, animal s ,tag tg, tags_pets tg_p where p.id = tg_p.pet AND tg.id = tg_p.tag AND tg.name = ? AND p.species = s.id order by p.id desc",[value])
    elif oby == "name":
        if order == "asc":
            cursor.execute("select p.id, p.name, p.bought, p.sold, s.name from pet p, animal s ,tag tg, tags_pets tg_p where p.id = tg_p.pet AND tg.id = tg_p.tag AND tg.name = ? AND  p.species = s.id order by p.name",[value])
        else:
            cursor.execute("select p.id, p.name, p.bought, p.sold, s.name from pet p, animal s ,tag tg, tags_pets tg_p where p.id = tg_p.pet AND tg.id = tg_p.tag AND tg.name = ? AND p.species = s.id order by p.name desc",[value])
    elif oby == "bought":
        if order == "asc":
            cursor.execute("select p.id, p.name, p.bought, p.sold, s.name from pet p, animal s ,tag tg, tags_pets tg_p where p.id = tg_p.pet AND tg.id = tg_p.tag AND tg.name = ? AND p.species = s.id order by p.bought",[value])
        else:
            cursor.execute("select p.id, p.name, p.bought, p.sold, s.name from pet p, animal s ,tag tg, tags_pets tg_p where p.id = tg_p.pet AND tg.id = tg_p.tag AND tg.name = ? AND p.species = s.id order by p.bought desc",[value])
    elif oby == "sold":
        if order == "asc":
            cursor.execute("select p.id, p.name, p.bought, p.sold, s.name from pet p, animal s ,tag tg, tags_pets tg_p where p.id = tg_p.pet AND tg.id = tg_p.tag AND tg.name = ? AND  p.species = s.id order by p.sold",[value])
        else:
            cursor.execute("select p.id, p.name, p.bought, p.sold, s.name from pet p, animal s ,tag tg, tags_pets tg_p where p.id = tg_p.pet AND tg.id = tg_p.tag AND tg.name = ? AND  p.species = s.id order by p.sold desc",[value])
    elif oby == "species":
        if order == "asc":
            cursor.execute("select p.id, p.name, p.bought, p.sold, s.name from pet p, animal s ,tag tg, tags_pets tg_p where p.id = tg_p.pet AND tg.id = tg_p.tag AND tg.name = ? AND p.species = s.id order by p.species",[value])
        else:
            cursor.execute("select p.id, p.name, p.bought, p.sold, s.name from pet p, animal s ,tag tg, tags_pets tg_p where p.id = tg_p.pet AND tg.id = tg_p.tag AND tg.name = ? AND p.species = s.id order by p.species desc",[value])

    pets = cursor.fetchall()
    return pets
@bp.route("/search/<field>/<value>")
def search(field, value):
    # TBD
    conn = db.get_db()
    cursor = conn.cursor()
    oby = request.args.get("order_by", "id") # DONE
    order = request.args.get("order", "asc")
    pets=pets_filter_by(cursor,oby,order,field,value)
    cursor.close()
    return render_template('search.html', pets = pets,field = field, value = value, order="desc" if order=="asc" else "asc")

@bp.route("/")
def dashboard():
    conn = db.get_db()
    cursor = conn.cursor()
    oby = request.args.get("order_by", "id") # DONE
    order = request.args.get("order", "asc")
    pets=pets_order_by(cursor,oby,order)
    cursor.close()
    return render_template('index.html', pets = pets, order="desc" if order=="asc" else "asc")


@bp.route("/<int:pid>")
def pet_info(pid): 
    conn = db.get_db()
    cursor = conn.cursor()
    cursor.execute("select p.name, p.bought, p.sold, p.description, s.name from pet p, animal s where p.species = s.id and p.id = ?", [pid])
    pet = cursor.fetchone()
    cursor.execute("select t.name from tags_pets tp, tag t where tp.pet = ? and tp.tag = t.id", [pid])
    tags = (x[0] for x in cursor.fetchall())
    name, bought, sold, description, species = pet
    print(format_date(sold))#this of type none
    data = dict(id = pid,
                name = name,
                bought = format_date(bought),
                sold = format_date(sold),
                description = description, #DONE
                species = species,
                tags = tags)
    return render_template("petdetail.html", **data)

@bp.route("/<int:pid>/edit", methods=["GET", "POST"])
def edit(pid):
    conn = db.get_db()
    cursor = conn.cursor()
    if request.method == "GET":
        cursor.execute("select p.name, p.bought, p.sold, p.description, s.name from pet p, animal s where p.species = s.id and p.id = ?", [pid])
        pet = cursor.fetchone()
        cursor.execute("select t.name from tags_pets tp, tag t where tp.pet = ? and tp.tag = t.id", [pid])
        tags = (x[0] for x in cursor.fetchall())
        name, bought, sold, description, species = pet
        data = dict(id = pid,
                    name = name,
                    bought = format_date(bought),
                    sold = format_date(sold),
                    description = description,
                    species = species,
                    tags = tags)
        return render_template("editpet.html", **data)
    elif request.method == "POST":
        description = request.form.get('description')
        sold = request.form.get("sold")
        if sold:#value returned is "sold"
            sold = datetime.date.today()#.strftime("%a - %b %d, %Y")
        cursor.execute("UPDATE pet SET sold = ? , description = ? WHERE id = ?",[sold,description,pid])
        cursor.close()
        conn.commit()
        return redirect(url_for("pets.pet_info", pid=pid), 302)
        
    



