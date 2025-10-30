from flask import Flask, request, jsonify, render_template_string
import json
import os
from flask_cors import CORS
from datetime import datetime
app = Flask(__name__)
CORS(app)
app.config["JSON_AS_ASCII"] = False
app.config['JSON_SORT_KEYS'] = False 
mediaserver = 'https://raw.githubusercontent.com/thanhnho417/up/refs/heads/main'

def web_load_json(file):
    datadir = os.path.dirname(__file__)
    maindatadir = os.path.join(datadir, 'assets', file)
    with open(maindatadir, 'r', encoding='utf-8') as f:
        return json.load(f)

@app.route('/')
def welcome_to_my_server():
    return jsonify({'title': 'Xin chao may chau'})




@app.route('/getpageinfo')
def page_web_content():
    page_tab = request.args.get('p')
    web_tab_file_name = {
        'home': 'web_home.json',
        'introduce': 'web_introduce.json',
        'game': 'web_game.json',
        'multimedia': 'web_multimedia.json',
        'anime': 'web_ani.json',
        'blog': 'web_blog.json',
        'link': 'web_link.json',
        'project': 'web_project.json'
    }

    if not page_tab or page_tab not in web_tab_file_name:
        return '<h3>Không có dữ liệu</h3>'
    
    web_data = web_load_json(web_tab_file_name[page_tab])
    web_content = web_data
    if page_tab == 'home':
        return jsonify(web_content)
    elif page_tab == 'introduce':
        return jsonify(web_content)
    elif page_tab == 'game':
        game_publisher = request.args.get('publisher')
        if not game_publisher: 
            publisher_game_item = {
                'web_title': web_content.get('web_title', '')
            }
            for i, j in web_content.items():
                web_game_publisher = {}
                game_publisher_item = {}
                if i in('web_title'): continue
                if not isinstance(j, dict): continue
                web_game_publisher[i] = {
                    'game_publisher_title': j.get('game_publisher_title', '')
                }
                print(j)
                for m,n in j.items():
                    print(n)
                    if not isinstance(n, dict): continue
                    game_publisher_item[m] = {
                        'title': n.get('title', ""),
                        'thumbnail': n.get('thumbnail', '')
                    }
                    web_game_publisher[i].update(game_publisher_item)
                publisher_game_item.update(web_game_publisher)
            return publisher_game_item
        else:
            game_publisher_id = request.args.get('id')
            if not game_publisher_id:
                game_list = web_content.get(game_publisher, '')
                web_game_publisher_item = {
                    'game_publisher_title': game_list.get('game_publisher_title', '')
                }
                game_publisher_item = {}
                for i, j in game_list.items():
                    if not isinstance(j, dict): continue
                    game_publisher_item[i] = {
                        'title': j.get('title', ''),
                        'thumbnail': j.get('thumbnail', '')    
                    }
                    web_game_publisher_item.update(game_publisher_item)
                return web_game_publisher_item
            else:
                return (web_content.get(game_publisher, "")).get(game_publisher_id, '')
    elif page_tab == 'multimedia':
        mul_type = request.args.get('type')
        if not mul_type: 
            web_mul_type = {'type': {m_type: "" for m_type in web_content['type'].keys()}, 'web_title': web_content['web_title'], 'web_trans': web_content['web_trans']}
            return web_mul_type
        else:
            if mul_type == 'video':
                web_mul_vid_id = request.args.get('id')
                if not web_mul_vid_id: 
                    mul_vid_list = (web_content.get('type', "")).get(mul_type, "")
                    mul_vid_list_id = {}
                    for i,j in mul_vid_list.items():
                        if i == 'web_title': continue
                        mul_vid_list_id[i] = {
                            "title": j.get('title', ""),
                            "thumbnail": j.get('thumbnail', ""),
                            "date": j.get('date', "")
                        }
                    
                    web_mul_vid_id_list = {'web_title': mul_vid_list.get('web_title', "")}
                    web_mul_vid_id_list.update(dict(sorted(mul_vid_list_id.items(), key=lambda x: datetime.strptime(x[1].get('date', '01/01/1970'), "%d/%m/%Y"), reverse=True)))
                    return json.dumps(web_mul_vid_id_list, ensure_ascii=False, sort_keys=False)
                else:
                    mul_vid_list_id_item = ((web_content.get('type', '')).get(mul_type, '')).get(web_mul_vid_id, '')
                    return mul_vid_list_id_item
                    
    elif page_tab == 'anime':
        ani_year = request.args.get('y')
        if not ani_year:
            web_ani_year_list = {"year": {year: {} for year in web_content["year"].keys()}, "web_title": web_content["web_title"]}
            return jsonify(web_ani_year_list)
        else:
            if ani_year not in web_content.get("year", {}):
                return jsonify({"season": "Không có sẵn"})
            else:
                ani_season = request.args.get('ss')
                if not ani_season:
                    web_ani_year_season = web_content.get("year", {})
                    web_ani_year_season_list = {"web_title": web_ani_year_season[ani_year]["web_title"], "web_trans": web_ani_year_season[ani_year]["web_trans"], "season": {ss: {} for ss in web_ani_year_season[ani_year]["season"].keys()}}
                    return json.dumps(web_ani_year_season_list, ensure_ascii=False, sort_keys=False)
                else:
                    ani_year_season_id = request.args.get('id')
                    if not ani_year_season_id:
                        web_ani_year_season_id = (((web_content.get("year", {})).get(ani_year, {})).get("season", {})).get(ani_season, {})
                        web_ani_year_season_id_list = {}
                        for i, j in web_ani_year_season_id.items():
                            if i in("web_title", "web_trans"): continue
                            if not isinstance(j, dict): continue
                            if "web_ani_title" not in j: continue
                            web_ani_year_season_id_list[i] = {
                                "web_ani_title": j.get("web_ani_title", ""),
                                "web_ani_img": j.get("web_ani_img", ""),
                                "web_ani_color_bg": j.get("web_ani_color_bg", ""),
                                "web_ani_color": j.get("web_ani_color", "")
                            }
                        web_ani_year_season_id_title = {"web_title": web_ani_year_season_id.get("web_title")}
                        web_ani_year_season_id_list.update(web_ani_year_season_id_title)
                        return web_ani_year_season_id_list
                    else:
                        web_ani_year_season_id_info = ((((web_content.get("year", {})).get(ani_year, {})).get("season", {})).get(ani_season, {})).get(ani_year_season_id, {})
                        return web_ani_year_season_id_info


    elif page_tab == 'link':
        return jsonify(web_content)
    elif page_tab == 'blog':
        return jsonify(web_content)
    elif page_tab == 'project':
        return jsonify(web_content)




































    

if __name__ == "__main__":
    app.run(debug=True, port=4040)