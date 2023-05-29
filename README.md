# Rh positive blood type distribution worldwide
#### Video Demo:  <[DEMO](https://www.youtube.com/watch?v=XQXZ1I_Chd8)>
#### Description:
<p>The project is about visualization of blood type distribution by country.The project is hosted on pythonanywhere.com and the domain name is [bloodtypes.net](https://www.bloodtypes.net/). I used data from <[Wikipedia](https://en.wikipedia.org/wiki/Blood_type_distribution_by_country)> to generate interactive maps and graphs using folium.Choropleth. I’ve also added the functionality for users to submit their blood type, save it in a CSV file, and display the updated map from user-submitted data.</p>

<p>The  project is written in Flask, using Python. Here is the code to display maps from the data downloaded from [Wikipedia](https://en.wikipedia.org/wiki/Blood_type_distribution_by_country), which I converted to CSV file:</p>


```python
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
```


<p>Since Folium can compare only 2 columns, I made 4 functions and 4 paths to filter the data by blood types. That was the easy part. The hard part was to write the code to get data from users and display the updated map. Here is the code:</p>



```python
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
```
<p>The hardest part was to write the code below, after hundreds of errors and tries and it took me about a week to figure out the correct code.</p>
    
```python
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
```

<p>I've also generated the graph using the code below:</p>

```python
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
```

<p>Then I made a screenshot of the generated graph and put the image file in index.html so the first page could load faster. I have also merged maps filtered by the different blood types, which are also displayed in an index.html.</p>

<p>I have also added the feedback.html file, which I made using Google Forms. I would have made it myself, but I don’t have PHP installed on my remote server at pythonanywhere.com. Besides, Google Forms are easy and nice. Fortunatly domain name bloodtypes.net was not taken and it was cheap.</p>

<p>It took me around 4 weeks to finish the project. It was challenging, but I learned a lot.</p>
    <p>[And here is the git link of the project]( https://github.com/rarikola/bloodtypes.git)</p>
