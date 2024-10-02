from flask import (
    Flask, 
    jsonify, 
    render_template,
    request)
import os
import json
import mimetypes
from utils.DIDreader import DIDReader

ROOT_DIR = os.path.abspath(os.getcwd())

class Pratto:
    def list_files(self, dirname=None):
        if os.path.exists(dirname):
            return [
            f"{dirname}/{filename}" for filename in os.listdir(f"{dirname}")
            if "excel" in mimetypes.guess_type(filename)[0]
            ]
        return []




pratto_actions = Pratto()

app = Flask(
    __name__, 
    template_folder = "templates",
    static_folder = "statics"
    
    )

DEF_CONFIG = ['DID', 'DIAG', 'DE']

@app.route('/')
def initial():

    return render_template("index.html")

@app.route('/load_fts/', methods = ['POST'])
def load_fts():
    mdx = request.files["mdx"]
    did_class = DIDReader(mdx)
    did_class.read_mdx()
    de00 = did_class.get_config(config='de01')
    serie = did_class.get_bus(de00)
    assert False, serie
    applies = [
        "MY25 S832 Gold",
        "MY25 CX720 ",
        "MY24 S832 Gold",
        ]
    return render_template("lista.html", applies=applies)


@app.route('/fts/', methods = ['POST','GET'])
def list_fts():

    total = []

    for i in range(30):
        po =[
        ("Selectable Drive Mode_Cfg DE05",0x1),
        ("Brand_Cfg [DE0B]","0x0"),
        ("SelDrvMde_D2Rq",0x0),
        ("SelDrvMde_D2_Rq",0x0),
        ("SelDrvMdeMsgTxt_D_Rq",0x1),
        ("SelDrvMdePos01_B_Avail",0x1),
        ("SelDrvMdePos01_D_Stat",0x0),
         ("ActvDrvMde_D2_Stat",i)
          ]
        total.append(po)
    return render_template("fts.html", total=total)



@app.route('/runner/<int:idtest>', methods = ['GET'])
def fun_tc(idtest):

    return jsonify({'run':True})




    assert False, df
    assert False, dir(data)
    return jsonify({'operation pratto':ROOT_DIR})
