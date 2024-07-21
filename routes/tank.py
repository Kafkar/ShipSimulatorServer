from flask import render_template, request, jsonify

def register_tank_routes(app, tank_control):
    @app.route('/tank', methods=['GET', 'POST'])
    def tank_level():
        if request.method == 'POST':
            level = request.form.get('level', type=int)
            tank_control.set_level(level)
            return jsonify({"success": True, "level": level})
        elif request.method == 'GET':
            level = tank_control.get_level()
            return jsonify({"level": level})
        return render_template('tank.html', level=tank_control.get_level())
