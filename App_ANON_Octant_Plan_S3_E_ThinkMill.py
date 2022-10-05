# TO DO

import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from datetime import datetime
import streamlit as st
from datetime import date
import streamlit as st
import copy
import streamlit_authenticator as stauth
import yaml
import os
import pyotp
import time
import plotly.graph_objects as go



def set_bg_hack_url():
    '''
    A function to unpack an image from url and set as bg.
    Returns
    -------
    The background.
    '''
        
    st.markdown(
         f"""
         <style>
         .stApp {{
             background: url("https://public-octant-files.s3.ap-southeast-2.amazonaws.com/OctantAI_background_white.jpg");
             #background: url("https://public-octant-files.s3.ap-southeast-2.amazonaws.com/OctantAI_background_teal.jpg");
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )


st.set_page_config(page_title="For Thinkmill ")

tab1, tab2, tab3, tab4 = st.tabs(["Logon/ Logoff", "Load data", "Model", "Results"])

# Suppress the Streamlit watermark and hamburger
set_bg_hack_url() #Set the background image
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

#st.write('\n generated_data', generated_data)    

with tab1:
    
    import streamlit as st
    
    #user_OTP_code = generate_URI_QR_code()
    src = str(os.path.join('C:/', 'Users/', 'config.yml'))
    with open(src) as file:
        config = yaml.safe_load(file) #, Loader=SafeLoader)
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['preauthorized']
    )
    name, authentication_status, username = authenticator.login('Login', 'main')
    
    
    if authentication_status:
        #st.write(f'Please enter the code from your Microsoft Authenticator app before it expires to continue {name}')
        #st.write('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
        st.success('Logged in successfully')
        st.balloons()
        authenticator.logout('Logout', 'main')
    elif authentication_status == False:
        st.error('Username/password is incorrect')
    elif authentication_status == None:
        st.warning('Please enter your username and password')


with tab2:
    if authentication_status == False or authentication_status == None:
        st.error('Please log in first')
    else:
        st.header("Load data")

        uploaded_file1 = st.file_uploader("Load project data in Excel format ")

        if uploaded_file1 is not None:
            #shows1 = pd.read_csv(uploaded_file1, encoding= 'unicode_escape') #shows is a dataframe
            shows1 = pd.read_excel(uploaded_file1) #shows is a dataframe
            uploaded_file1.seek(0)
            st.success('Load successful. Preview your file below.')
            st.write(shows1)

with tab3:
    if authentication_status == False or authentication_status == None:
        st.error('Please log in first')
    else:
        st.header("Model")
        if uploaded_file1 == None:
            st.error('Please load data')
        else:
            project_A = copy.deepcopy(shows1)
            project_A = project_A.dropna()
            project_A_cost_modelling = project_A[project_A['cost_model_status'].isin(['Include'])]#,'TEI'])]
            new_df_project_A = project_A_cost_modelling
            project_A_cost_modelling_direct_costs = project_A_cost_modelling['totalcost'].sum()
            
            
            df_project_A = pd.DataFrame(project_A)
            
            
            # Fine tune your project
            st.subheader('Custom risk tuning ')
            st.write('As an option, you can fine-tune the prediction using your knowledge about the project risk factors.')          
            st.write('For each of the below project risk factors, rank them based on your judgement for your project')
            st.write('0 = Well below average, 1 = Below average, 2 = About average, 3 = Above average, 4 = Well above average ')
            definition = st.slider('How mature is the overall upfront definition of the project?', 0,4,2)
            scope = st.slider('How well defined is the scope of the project?', 0,4,2)
            tech_complexity = st.slider('How well managed is the technical complexity on this project?', 0,4,2)
            social_complexity = st.slider('How well managed is the social complexity on this project?', 0,4,2)
            pace = st.slider('How well managed is the pace of this project?', 0,4,2)
            novelty = st.slider('How well managed are any novel technologies on this project?', 0,4,2)
            team = st.slider('What is the quality of the internal delivery team on this project?', 0,4,2)
            contractors = st.slider('What is the quality of the external construction contractors on this project?', 0,4,2)
            geotech = st.slider('What is the quality of the geotechnical investigations undertaken on this project?', 0,4,2)
            latent = st.slider('How well defined are the latent conditions on this project?', 0,4,2)
            risk_score = 45 - (definition + scope + tech_complexity + social_complexity + pace + novelty + team + contractors + geotech + latent)
            st.write('risk_score', risk_score)
            risk_uplift = int(round(risk_score / 40 * (95/5 - 5/5)) * 5)
            st.write('risk_uplift',risk_uplift)
            fig = go.Figure(data=go.Scatterpolar(
              r=[definition, scope, tech_complexity, social_complexity, pace, novelty, team, contractors, geotech, latent],
              theta=['definition','scope','technical complexity', 'social complexity','pace', 'novelty','team','contractors','geotechnical investigations','other latent conditions'],
              fill='toself'
            ))

            fig.update_layout(
              polar=dict(
                radialaxis=dict(
                  visible=True
                ),
              ),
              showlegend=False
            )
            st.write('Project risk chart')
            st.plotly_chart(fig, use_container_width=True)


with tab4:
    if authentication_status == False or authentication_status == None:
        st.error('Please log in first')
    else:
        st.header("Results")
        if uploaded_file1 == None:
            st.error('Please load data')
        else:
            if uploaded_file1 is not None:

                project_A_cost_modelling = new_df_project_A 
                project_A_TEI = 225


                Level_of_Certainty = [5, 10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95]
                Adjustment_Required = [-0.249847683, -0.113676947, -0.043385359, 0.027936416, 
                                       0.092926754, 0.032837742, 0.077995318, 0.121823767,
                                       0.216275251, 0.239945131,0.266237311, 0.250750516,
                                       0.361998798, 0.549025344,0.738236778,1.004627822,
                                       1.496675929,2.242933464,2.957109458]
                
                
                dict_top_down_uplift = dict(zip(Level_of_Certainty, Adjustment_Required))
                
                top_down_uplift = dict_top_down_uplift[55]
                top_down_uplift_risk = dict_top_down_uplift[risk_uplift]
                project_A_top_down = project_A_cost_modelling_direct_costs * (1+top_down_uplift)
                project_A_risk_adjusted = project_A_cost_modelling_direct_costs * (1 + top_down_uplift_risk)
                               
                
                total_expected_investment = [project_A_TEI]
                Top_Down_estimate = [project_A_top_down]
                Risk_Adjusted_estimate = [project_A_risk_adjusted]
                index = ['Project_A']

                df = pd.DataFrame({'Final Cost Estimate': total_expected_investment,
                                   'Octant estimate (P50)': Top_Down_estimate,
                                   'Your custom risk-adjusted estimate': Risk_Adjusted_estimate}, index=index)
                ax = df.plot(kind='bar', title='Comparing Final Business Case, Octant and User Risk adjusted estimates\n      ', figsize=(6,6), color=['#013C4C','#1898D5','#6ABE4E'])
                ax.set_xlabel("Project")
                ax.set_ylabel("$M Cost Forecast")
                plt.show()
                ax.legend(bbox_to_anchor=(1.1, 1.05))
                st.pyplot(plt)
                st.markdown('----')
                st.subheader('So what is being demonstrated here?')
                st.write(
                    'Firstly we demonstrate a simple log on widget. Multifactor authentication is not shown for deployment simplicity reasons.')
                st.write(
                    'Next, we show a simple file loading widget. To keep deployment simple, the example file has been shared with Thinkmill for loading from local machines. ')
                st.write(
                    'The risk sliders are intended to show one way that users can produce an additional, complementary Octant output that incorporates user knowledge about the target project.')
                st.write(
                    'The radar chart is a simple way to visualise the risk "thumbprint" for the project that embeds the users belief about the project risk profile.')
                st.write(
                    'The risk factors used in this demo were sourced from peer-reviewed research, but are easy to customise for the user if required (as a premium option).')
                st.write(
                    'The concept behind the sliders is that the more favourable and less risky the project conditions for execution, the lower the cost uplift needs to be.')
                st.write(
                    'The graph above illustrates how the risk sliders now allow for a third reporting option that now incorporates user knowledge, and allows them to control the level of reporting '
                    'that the PM provides.')
                st.write(
                    'For instance, if the user thinks the Octant forecast is too high/ conservative, the user can adjust the sliders until it reflects their beliefs about the unique risk circumstances'
                    'of the project. This dynamically updates the cost forecast.')





                
                





                


