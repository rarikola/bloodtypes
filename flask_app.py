from flask import Flask, render_template,redirect, session, url_for
import csv
import pandas as pd
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import folium
from flask_wtf import FlaskForm
import secrets

# Generate a random secret key
secret_key = secrets.token_hex(16)  # 16 bytes = 32 hex characters

app = Flask(__name__)
# Set the secret key in your Flask app's configuration
app.config['SECRET_KEY'] = secret_key

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/a")
def a():
    return render_template("a.html")

@app.route("/b")
def b():
    return render_template("b.html")

@app.route("/o")
def o():
    return render_template("o.html")

@app.route("/ab")
def ab():
    return render_template("ab.html")

@app.route("/feedback")
def feedback():
    return render_template("feedback.html")

@app.route('/test', methods=['GET', 'POST'])
def form():
    form = MyForm()

    if form.validate_on_submit():
        country = form.country.data
        blood_type = form.blood_type.data

        # Check if the user has already submitted the form
        if session.get('submitted'):
            return redirect('/test')

        # Update the CSV file
        update_csv(country, blood_type)

        # Mark the form as submitted
        session['submitted'] = True

        return redirect('/test')
    print(form.blood_type.data)
    return render_template('form.html', form=form, submitted=session.get('submitted'), blood_type=form.blood_type.data)

def update_csv(country, blood_type):
    # Open the CSV file and read its contents
    with open('/home/rarikola/bloodtypes/test/data.csv', 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)

    # Find the row corresponding to the selected country
    if rows:
        for row in rows:
            if row and row[0].strip() == country.strip():
                # Update the blood type count
                blood_type_index = ['O', 'A', 'B', 'AB'].index(blood_type)
                row[blood_type_index + 1] = str(int(row[blood_type_index + 1]) + 1)
                break
        else:
            # If the country is not found, create a new row
            new_row = [country] + ['0'] * 4
            blood_type_index = ['O', 'A', 'B', 'AB'].index(blood_type)
            new_row[blood_type_index + 1] = '1'
            rows.append(new_row)
    else:
        # If the file is empty, create a new row
        new_row = [country] + ['0'] * 4
        blood_type_index = ['O', 'A', 'B', 'AB'].index(blood_type)
        new_row[blood_type_index + 1] = '1'
        rows.append(new_row)

    # Write the updated contents back to the CSV file
    with open('/home/rarikola/bloodtypes/test/data.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)

class MyForm(FlaskForm):
    country = SelectField('Country', validators=[DataRequired()], choices=[
            ("	Albania	","	Albania	"),
            ("	Algeria	","	Algeria	"),
            ("	Argentina	","	Argentina	"),
            ("	Armenia	","	Armenia	"),
            ("	Australia	","	Australia	"),
            ("	Austria	","	Austria	"),
            ("	Azerbaijan	","	Azerbaijan	"),
            ("	Bahrain	","	Bahrain	"),
            ("	Bangladesh	","	Bangladesh	"),
            ("	Belarus	","	Belarus	"),
            ("	Belgium	","	Belgium	"),
            ("	Bhutan	","	Bhutan	"),
            ("	Bolivia	","	Bolivia	"),
            ("	Bosnia and Herzegovina	","	Bosnia and Herzegovina	"),
            ("	Brazil	","	Brazil	"),
            ("	Bulgaria	","	Bulgaria	"),
            ("	Burkina Faso	","	Burkina Faso	"),
            ("	Cambodia	","	Cambodia	"),
            ("	Cameroon	","	Cameroon	"),
            ("	Canada	","	Canada	"),
            ("	Chile	","	Chile	"),
            ("	China	","	China	"),
            ("	Colombia	","	Colombia	"),
            ("	Costa Rica	","	Costa Rica	"),
            ("	Croatia	","	Croatia	"),
            ("	Cuba	","	Cuba	"),
            ("	Cyprus	","	Cyprus	"),
            ("	Czech Republic	","	Czech Republic	"),
            ("	Democratic Republic of the Congo	","	Democratic Republic of the Congo	"),
            ("	Denmark	","	Denmark	"),
            ("	Dominican Republic	","	Dominican Republic	"),
            ("	Ecuador	","	Ecuador	"),
            ("	Egypt	","	Egypt	"),
            ("	El Salvador	","	El Salvador	"),
            ("	Estonia	","	Estonia	"),
            ("	Ethiopia	","	Ethiopia	"),
            ("	Fiji	","	Fiji	"),
            ("	Finland	","	Finland	"),
            ("	France	","	France	"),
            ("	Gabon	","	Gabon	"),
            ("	Georgia	","	Georgia	"),
            ("	Germany	","	Germany	"),
            ("	Ghana	","	Ghana	"),
            ("	Greece	","	Greece	"),
            ("	Guinea	","	Guinea	"),
            ("	Honduras	","	Honduras	"),
            ("	Hong Kong	","	Hong Kong	"),
            ("	Hungary	","	Hungary	"),
            ("	Iceland	","	Iceland	"),
            ("	India	","	India	"),
            ("	Indonesia	","	Indonesia	"),
            ("	Iran	","	Iran	"),
            ("	Iraq	","	Iraq	"),
            ("	Ireland	","	Ireland	"),
            ("	Israel	","	Israel	"),
            ("	Italy	","	Italy	"),
            ("	Ivory Coast	","	Ivory Coast	"),
            ("	Jamaica	","	Jamaica	"),
            ("	Japan	","	Japan	"),
            ("	Jordan	","	Jordan	"),
            ("	Kazakhstan	","	Kazakhstan	"),
            ("	Kenya	","	Kenya	"),
            ("	Laos	","	Laos	"),
            ("	Latvia	","	Latvia	"),
            ("	Lebanon	","	Lebanon	"),
            ("	Libya	","	Libya	"),
            ("	Liechtenstein	","	Liechtenstein	"),
            ("	Lithuania	","	Lithuania	"),
            ("	Luxemburg	","	Luxemburg	"),
            ("	Macao	","	Macao	"),
            ("	Malaysia	","	Malaysia	"),
            ("	Malta	","	Malta	"),
            ("	Mauritania	","	Mauritania	"),
            ("	Mauritius	","	Mauritius	"),
            ("	Mexico	","	Mexico	"),
            ("	Moldova	","	Moldova	"),
            ("	Mongolia	","	Mongolia	"),
            ("	Morocco	","	Morocco	"),
            ("	Myanmar	","	Myanmar	"),
            ("	Namibia	","	Namibia	"),
            ("	Nepal	","	Nepal	"),
            ("	Netherlands	","	Netherlands	"),
            ("	New Zealand	","	New Zealand	"),
            ("	Nicaragua	","	Nicaragua	"),
            ("	Nigeria	","	Nigeria	"),
            ("	North Korea	","	North Korea	"),
            ("	North Macedonia	","	North Macedonia	"),
            ("	Norway	","	Norway	"),
            ("	Pakistan	","	Pakistan	"),
            ("	Papua New Guinea	","	Papua New Guinea	"),
            ("	Paraguay	","	Paraguay	"),
            ("	Peru	","	Peru	"),
            ("	Philippines	","	Philippines	"),
            ("	Poland	","	Poland	"),
            ("	Portugal	","	Portugal	"),
            ("	Romania	","	Romania	"),
            ("	Russia	","	Russia	"),
            ("	Saudi Arabia	","	Saudi Arabia	"),
            ("	Serbia	","	Serbia	"),
            ("	Singapore	","	Singapore	"),
            ("	Slovakia	","	Slovakia	"),
            ("	Slovenia	","	Slovenia	"),
            ("	Somalia	","	Somalia	"),
            ("	South Africa	","	South Africa	"),
            ("	South Korea	","	South Korea	"),
            ("	Spain	","	Spain	"),
            ("	Sri Lanka	","	Sri Lanka	"),
            ("	Sudan	","	Sudan	"),
            ("	Sweden	","	Sweden	"),
            ("	Switzerland	","	Switzerland	"),
            ("	Syria	","	Syria	"),
            ("	Taiwan	","	Taiwan	"),
            ("	Thailand	","	Thailand	"),
            ("	Tunisia	","	Tunisia	"),
            ("	Turkey	","	Turkey	"),
            ("	Uganda	","	Uganda	"),
            ("	Ukraine	","	Ukraine	"),
            ("	United Arab Emirates	","	United Arab Emirates	"),
            ("	United Kingdom	","	United Kingdom	"),
            ("	United States	","	United States	"),
            ("	Uzbekistan	","	Uzbekistan	"),
            ("	Venezuela	","	Venezuela	"),
            ("	Vietnam	","	Vietnam	"),
            ("	Yemen	","	Yemen	"),
            ("	Zimbabwe	","	Zimbabwe	")
    ])
    blood_type = SelectField('Blood Type', choices=[('A', 'A'), ('B', 'B'), ('AB', 'AB'), ('O', 'O')])
    submit = SubmitField('Submit')


@app.route("/typeo")
def typeo():
    df = pd.read_csv("/home/rarikola/bloodtypes/oabab.csv", delimiter=',')
    df.columns = df.columns.str.strip()
    political_countries_url = (
        "http://geojson.xyz/naturalearth-3.3.0/ne_50m_admin_0_countries.geojson"
    )

    m = folium.Map(location=(30, 10), zoom_start=3, tiles="cartodb positron")
    folium.Choropleth(
        geo_data=political_countries_url,
        data=df,
        columns=("Country", "O"),
        key_on="feature.properties.name",
        fill_color="Oranges",
        fill_opacity=0.8,
        line_opacity=0.4,
        nan_fill_color="white",
        legend_name="O+ Blood type distribution by country",
    ).add_to(m)

    m.save("/home/rarikola/bloodtypes/templates/typeo.html")

    return render_template("typeo.html")

@app.route("/typea")
def typea():
    df = pd.read_csv("/home/rarikola/bloodtypes/oabab.csv", delimiter=',')
    df.columns = df.columns.str.strip()
    political_countries_url = (
        "http://geojson.xyz/naturalearth-3.3.0/ne_50m_admin_0_countries.geojson"
    )

    m = folium.Map(location=(30, 10), zoom_start=3, tiles="cartodb positron")
    folium.Choropleth(
        geo_data=political_countries_url,
        data=df,
        columns=("Country", "A"),
        key_on="feature.properties.name",
        fill_color="Greens",
        fill_opacity=0.8,
        line_opacity=0.4,
        nan_fill_color="white",
        legend_name="A+ Blood type distribution by country",
    ).add_to(m)


    m.save("/home/rarikola/bloodtypes/templates/typea.html")

    return render_template("typea.html")

@app.route("/typeb")
def typeb():
    df = pd.read_csv("/home/rarikola/bloodtypes/oabab.csv", delimiter=',')
    df.columns = df.columns.str.strip()
    political_countries_url = (
        "http://geojson.xyz/naturalearth-3.3.0/ne_50m_admin_0_countries.geojson"
    )

    m = folium.Map(location=(30, 10), zoom_start=3, tiles="cartodb positron")
    folium.Choropleth(
        geo_data=political_countries_url,
        data=df,
        columns=("Country", "B"),
        key_on="feature.properties.name",
        fill_color="Blues",
        fill_opacity=0.8,
        line_opacity=0.4,
        nan_fill_color="white",
        legend_name="B+ Blood type distribution by country",
    ).add_to(m)


    m.save("/home/rarikola/bloodtypes/templates/typeb.html")

    return render_template("typeb.html")

@app.route("/typeab")
def typeab():
    df = pd.read_csv("/home/rarikola/bloodtypes/oabab.csv", delimiter=',')
    df.columns = df.columns.str.strip()
    political_countries_url = (
        "http://geojson.xyz/naturalearth-3.3.0/ne_50m_admin_0_countries.geojson"
    )

    m = folium.Map(location=(30, 10), zoom_start=3, tiles="cartodb positron")
    folium.Choropleth(
        geo_data=political_countries_url,
        data=df,
        columns=("Country", "AB"),
        key_on="feature.properties.name",
        fill_color="Purples",
        fill_opacity=0.8,
        line_opacity=0.4,
        nan_fill_color="white",
        legend_name="AB+ Blood type distribution by country",
    ).add_to(m)


    m.save("/home/rarikola/bloodtypes/templates/typeab.html")

    return render_template("typeab.html")

@app.route('/graphs')
def plot_graph():
    # Load the data from a CSV file
    df = pd.read_csv("/home/rarikola/bloodtypes/oabab.csv", delimiter=',')
    df.columns = df.columns.str.strip()

    # Create the bar plot
    plt.rcParams.update({'font.size': 9})
    plt.figure(figsize=(18, 8))
    plt.bar(df['Country'], df['O'], color='red', label='Type O', alpha=0.3)
    plt.bar(df['Country'], df['A'], color='blue', label='Type A', alpha=0.5)
    plt.bar(df['Country'], df['B'], color='green', label='Type B', alpha=0.7)
    plt.bar(df['Country'], df['AB'], color='yellow', label='Type AB', alpha=0.9)

    plt.xticks(rotation=90)
    plt.legend()

    # Save the plot to a BytesIO object
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Encode the plot image as base64
    plot_data = base64.b64encode(buffer.getvalue()).decode()
    buffer.close()

    # Render the template with the plot image
    return render_template('plot.html', plot_data=plot_data)

@app.route("/bto")
def bto():
    df = pd.read_csv("/home/rarikola/bloodtypes/test/data.csv", delimiter=',')
    df.columns = df.columns.str.strip()
    political_countries_url = (
        "http://geojson.xyz/naturalearth-3.3.0/ne_50m_admin_0_countries.geojson"
    )

    m = folium.Map(location=(30, 10), zoom_start=3, tiles="cartodb positron")
    folium.Choropleth(
        geo_data=political_countries_url,
        data=df,
        columns=("Country", "O"),
        key_on="feature.properties.name",
        fill_color="Reds",
        fill_opacity=0.8,
        line_opacity=0.4,
        nan_fill_color="white",
        legend_name="O+ Blood type distribution by country",
    ).add_to(m)


    m.save("/home/rarikola/bloodtypes/templates/bto.html")

    return render_template("bto.html")

@app.route("/bta")
def bta():
    df = pd.read_csv("/home/rarikola/bloodtypes/test/data.csv", delimiter=',')
    df.columns = df.columns.str.strip()
    political_countries_url = (
        "http://geojson.xyz/naturalearth-3.3.0/ne_50m_admin_0_countries.geojson"
    )

    m = folium.Map(location=(30, 10), zoom_start=3, tiles="cartodb positron")
    folium.Choropleth(
        geo_data=political_countries_url,
        data=df,
        columns=("Country", "A"),
        key_on="feature.properties.name",
        fill_color="Greens",
        fill_opacity=0.8,
        line_opacity=0.4,
        nan_fill_color="white",
        legend_name="A+ Blood type distribution by country",
    ).add_to(m)


    m.save("/home/rarikola/bloodtypes/templates/bta.html")

    return render_template("bta.html")

@app.route("/btb")
def btb():
    df = pd.read_csv("/home/rarikola/bloodtypes/test/data.csv", delimiter=',')
    df.columns = df.columns.str.strip()
    political_countries_url = (
        "http://geojson.xyz/naturalearth-3.3.0/ne_50m_admin_0_countries.geojson"
    )

    m = folium.Map(location=(30, 10), zoom_start=3, tiles="cartodb positron")
    folium.Choropleth(
        geo_data=political_countries_url,
        data=df,
        columns=("Country", "B"),
        key_on="feature.properties.name",
        fill_color="Blues",
        fill_opacity=0.8,
        line_opacity=0.4,
        nan_fill_color="white",
        legend_name="B+ Blood type distribution by country",
    ).add_to(m)


    m.save("/home/rarikola/bloodtypes/templates/btb.html")

    return render_template("btb.html")

@app.route("/btab")
def btab():
    df = pd.read_csv("/home/rarikola/bloodtypes/test/data.csv", delimiter=',')
    df.columns = df.columns.str.strip()
    political_countries_url = (
        "http://geojson.xyz/naturalearth-3.3.0/ne_50m_admin_0_countries.geojson"
    )

    m = folium.Map(location=(30, 10), zoom_start=3, tiles="cartodb positron")
    folium.Choropleth(
        geo_data=political_countries_url,
        data=df,
        columns=("Country", "AB"),
        key_on="feature.properties.name",
        fill_color="Purples",
        fill_opacity=0.8,
        line_opacity=0.4,
        nan_fill_color="white",
        legend_name="AB+ Blood type distribution by country",
    ).add_to(m)


    m.save("/home/rarikola/bloodtypes/templates/btab.html")

    return render_template("btab.html")

