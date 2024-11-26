from flask import Flask, render_template, redirect, request, url_for
import requests

app = Flask( __name__ )

def pageNoFound( error ):
    return render_template( 'index.html' ), 404

@app.route( "/" )
def index():
    return render_template( 'index.html' )

@app.route( "/cines" )
@app.route( "/cines/<id>" )
def cines( id = None ):
    if id == None:
        response = requests.get( 'https://oaemdl.es/cinestar_sweb_php/cines' )
        if response.status_code == 200:
            response = response.json()
            if response[ 'success' ]:
                return render_template( 'cines.html', cines = response[ 'data' ] )
            else: return redirect( url_for( 'index' ))
        else: return redirect( url_for( 'index' ))
        
    else:
        if id.isdigit():
            response = requests.get( f"https://oaemdl.es/cinestar_sweb_php/cines/{id}" )
            if response.status_code == 200:
                response = response.json()
                if response[ 'success' ]:
                    return render_template( 'cine.html', cine = response [ 'data' ] )
                else: return redirect( url_for( 'index' ))
            else: return redirect( url_for( 'index' ))
            
        return redirect( url_for( 'index' ))

@app.route( "/peliculas/<id>" )
def peliculas( id ):
    if id == 'cartelera' or id == 'estrenos' or id.isdigit():
        response = requests.get( f"https://oaemdl.es/cinestar_sweb_php/peliculas/{id}" )
        if response.status_code == 200:
            response = response.json()
            if response[ 'success' ]:
                if id.isdigit():
                    return render_template( 'pelicula.html', pelicula = response [ 'data' ] )
                return render_template( 'peliculas.html', peliculas = response [ 'data' ] )
            else : return redirect( url_for( 'index' ))
        else : return redirect( 'index.html' )

    return redirect( url_for( 'index' ))

if __name__ == "__main__":
    app.register_error_handler( 404, pageNoFound) 
    app.run( debug = False )
    