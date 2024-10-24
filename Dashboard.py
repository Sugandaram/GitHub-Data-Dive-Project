import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title = 'Github Repositories!!!', page_icon = ":bar_chart:", layout = "wide")

st.title(":Github Repositories Project Visualization")
st.markdown('<style>div.block-container{padding-top:lrem;}</style>',unsafe_allow_html=True)
 
fl = st.file_uploader(":file_folder: upload a file", type = (["csv", "txt", "xlsx", "xls"]))
if fl is not None:
    filename = fl.name
    st.write(filename)
    df = pd.read_csv(filename, encoding = "ISO-8859-1")
else:
    df = pd.read_csv("Github_Repositories.csv", encoding = "ISO-8859-1")

col1, col2 = st.columns((2))
df['Creation Date'] = pd.to_datetime(df['Creation Date'])

#Getting the min and max date
Repostartdate = pd.to_datetime(df["Creation Date"]).min()
RepoUpdateddate = pd.to_datetime(df["Creation Date"]).max()


with col1:
    date1 = pd.to_datetime(st.date_input("Repostartdate", Repostartdate))

with col2:
    date2 = pd.to_datetime(st.date_input("RepoUpdateddate", RepoUpdateddate))

df = df[(df['Creation Date'] >=date1) & (df['Creation Date']<=date2)].copy()

st.sidebar.header("Choose your filter: ")
RepositoryName = st.sidebar.multiselect("Seclet Repository Name", df['Repository Name'].unique())

if not RepositoryName:
    df2 = df.copy()
else:
    df2 = df[df['Repository Name'].isin(RepositoryName)]

#Create for Programming Language

ProgrammingLanguage = st.sidebar.multiselect("Select Programming Language", df2['Programming Language'].unique())
if not ProgrammingLanguage:
    df3 = df2.copy()
else:
    df3 = df2[df2['Programming Language'].isin(ProgrammingLanguage)]


# Create for Owner

owner = st.sidebar.multiselect("Select Owner Name", df3['Owner'].unique())

# Filter the data based on Repository Name Programming Language and Owner

if not RepositoryName and not ProgrammingLanguage and not owner:
    filtered_df = df
elif not ProgrammingLanguage and not owner:
    filtered_df = df[df['Repository Name'].isin(RepositoryName)]
elif not RepositoryName and not owner:
    filtered_df = df[df["Programming Language"].isin(ProgrammingLanguage)]
elif ProgrammingLanguage and owner:
    filtered_df = df3[df["Programming Language"].isin(ProgrammingLanguage) & df3["Owner"].isin(owner)]
elif RepositoryName and owner:
    filtered_df = df3[df["Repository Name"].isin(RepositoryName) & df3["Owner"].isin(owner)]
elif RepositoryName and owner:
    filtered_df = df3[df["Repository Name"].isin(RepositoryName) & df3["Programming Language"].isin(ProgrammingLanguage)]
elif owner:
    filtered_df = df3[df3["Owner"].isin(owner)]
else:
    filtered_df = df3[df3["Repository Name"].isin(RepositoryName) & df3['Programming Language'].isin(ProgrammingLanguage) & df3['Owner'].isin(owner)]

stars_df = filtered_df.groupby(by = ['Number of Stars'], as_index = False)['Number of Forks'].sum()



with col1:
    st.subheader("Stars wise Forks")

    # Create a scatter plot
    fig = px.scatter(stars_df, x="Number of Stars", y="Number of Forks", template="seaborn")

    # Update layout to adjust the height and width of the chart
    fig.update_layout(height=300, width=500)  # Increased size

    # Display the chart in Streamlit with the correct parameter name
    st.plotly_chart(fig, use_container_width=False)  # Set use_container_width=False to use custom width


with col2:
    st.subheader('Repository Name wise Forks')
    
    # Correctly specifying 'x' and 'y' for box plot
    fig = px.line(filtered_df, x="Repository Name", y="Number of Forks")
    
    # Optional: You can update trace properties, though adding text to box plots might not display as intended
    fig.update_layout(height=450, width=500)
    
    # Displaying the plot in Streamlit
    st.plotly_chart(fig, use_container_width=True)

cl1, cl2 = st.columns((2))
with cl1:
    with st.expander("Stars_ViewData"):
        st.write(stars_df.style.background_gradient(cmap = "Blues"))
        csv = stars_df.to_csv(index = False).encode('utf-8')
        st.download_button("Download Data", data = csv, file_name = 'Number of Stars.csv', mime = 'text/csv', 
                          help = "Download the data as a CSV file")

with cl2:
     with st.expander("Repository Name View Data"):
        repository = filtered_df.groupby(by = "Repository Name", as_index = False)["Number of Forks"].sum()
        st.write(repository.style.background_gradient(cmap = "Oranges"))
        csv = repository.to_csv(index = False).encode('utf-8')
        st.download_button("Download Data", data = csv, file_name = 'Repository Name.csv', mime = 'text/csv', 
                          help = "Download the data as a CSV file")

filtered_df['month_year'] = filtered_df['Creation Date'].dt.to_period("M")
st.subheader("Time Series Analysis")

linechart = pd.DataFrame(filtered_df.groupby(filtered_df['month_year'].dt.strftime("%Y : %b"))['Number of Stars'].sum()).reset_index()
fig2 = px.line(linechart, x = "month_year", y = 'Number of Stars', labels = {'Number of Stars' : "Stars"}, height = 500, width = 1000, template = "gridon")
st.plotly_chart(fig2,use_container_with=True)

with st.expander("View Data of TimeSeries:"):
    st.write(linechart.T.style.background_gradient(cmap = "Blues"))
    csv = linechart.to_csv(index = False).encode("utf-8")
    st.download_button("Download Data", data = csv, file_name = "TimeSeries.csv", mime = 'text/csv')


# Create a tream based on Repository Name, Programming Language, and License Type
st.subheader("Hierarchical view of Stars using Treemap")
fig3 = px.treemap(filtered_df, path = ["Repository Name", "Programming Language", "License Type"], values = "Number of Stars", hover_data = ['Number of Stars'], color = "License Type")
fig3.update_layout(width = 800, height = 650)
st.plotly_chart(fig3, use_container_width = True)




    

