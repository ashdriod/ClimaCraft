from api.weather import get_weather


def get_weather_data_as_latex(location="Freiburg"):
    weather_data = get_weather(location)
    latex_content = """\\documentclass[12pt]{{article}}
    \\usepackage[utf8]{{inputenc}}
    \\usepackage{{hyperref}}
    \\usepackage{{graphicx}}
    \\usepackage{{fancyhdr}}
    \\usepackage{{geometry}}  % Adjusting document margins

    % Adjust document margins
    \\geometry{{left=1in, right=1in, top=1in, bottom=1in}}

    \\pagestyle{{fancy}}
    \\fancyhf{{}} % Clear all header and footer fields
    \\renewcommand{{\\headrulewidth}}{{0pt}} % No line in header
    \\renewcommand{{\\footrulewidth}}{{0pt}} % No line in footer

    % Custom title with bold and larger font
    \\title{{\\vspace{{-2cm}} % Adjust the vertical space as needed
           \\Huge\\textbf{{Clima Craft Report}} \\\\ [0.5cm]  % Making the title big and bold
           \\Large{{your lightweight LaTeX weather report}} % Subtitle in a slightly smaller size
           \\vspace{{0.5cm}} \\\\ \\hrule \\vspace{{-0.2cm}} \\hrule
    }}
    \\author{{}}
    \\date{{}}

    \\begin{{document}}
    \\maketitle
    \\fancyhead[L]{{\\textbf{{\\large Clima Craft Report}}}}  % Left header: Custom title, bold and larger
    """.format(location=location)

    if 'error' in weather_data:
        # Add error message if present
        latex_content += "\\section*{Error}\n" + weather_data['error']
    else:
        # Extract weather data
        temperature = weather_data['temperature_c']
        condition = weather_data['condition'].lower()
        wind_speed = weather_data['wind_kph']
        wind_direction = weather_data['wind_dir']
        pressure = weather_data['pressure_mb']
        humidity = weather_data['humidity']
        cloud_coverage = weather_data['cloud']
        feels_like = weather_data['feelslike_c']
        visibility = weather_data['visibility_km']

        # Detailed narratives for each aspect, including temperature
        temperature_narrative = ""
        if temperature <= 19:
            temperature_narrative = f"At a cool {temperature}°C, the air whispers of change, brisk and refreshing. It hints at the need for a warm layer, inviting a sense of calm and a breath of fresh air. This gentle reminder of the season's shift encourages one to savor the crispness that envelops the surroundings."
        elif 20 <= temperature <= 25:
            temperature_narrative = f"With the mercury at a pleasant {temperature}°C, there exists a perfect equilibrium. The temperature balances on the edge of warmth and coolness, creating an ideal backdrop for outdoor activities. It beckons one to fully embrace the day's potential, to live out moments amidst the gentle warmth that caresses the land."
        else:
            temperature_narrative = f"At a warm {temperature}°C, the area is enveloped in a warm embrace. It hints at lazy afternoons spent in the shade or the cool comfort of indoors, a testament to the sun's dominion. The day urges occasional ventures outside with care, to bask in the warmth while seeking solace in the cool shadows."

        # Integrate all narratives into a cohesive story
        detailed_narrative = f"""{temperature_narrative} Above, the skies of {location} don a cloak of {condition}, setting the stage for the day's mood. A wind, carrying whispers at {wind_speed} kph from the {wind_direction}, shapes the air's embrace. The atmosphere, pressing down with a pressure of {pressure} mb, remains unseen but deeply felt, a silent guardian of the day. Humidity at {humidity}% weaves a tale of invisible waters binding earth and sky, while clouds, those fleeting masterpieces, adorn {cloud_coverage}% of the heavens. This dance of light and shadow plays over the landscape, with the mercury hinting at {temperature}°C yet the sensation on the skin echoes {feels_like}°C. Visibility stretches to {visibility} km, promising clear views that invite the soul to wander. Together, these elements weave a tapestry of weather in {location}, not merely a story of data but an experience woven from the sun's warmth, the wind's caress, and the clouds' silent passage. Here, in the heart of {location}, the day unfolds with a promise of moments lived under an ever-changing sky, a narrative rich with the essence of life itself."""

        latex_content += "\\section*{Weather at a Glance }\n" + detailed_narrative

        latex_content += "\n\\paragraph{}This graph provides a clear idea about the temperature and precipitation in " + location + ".\n"
        latex_content += "\\begin{figure}[h]\n\\centering\n"
        latex_content += "\\includegraphics[width=0.8\\textwidth]{data/graph/temperature_precipitation_graph.png}\n"
        latex_content += "\\caption{Temperature and Precipitation Overview in " + location + "}\n"
        latex_content += "\\end{figure}\n"

    # Ensure the document is properly closed
    latex_content += "\n\\end{document}"
    return latex_content
