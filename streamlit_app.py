import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
import plotly.express as px
import pandas as pd

# Sidebar with useful links
st.sidebar.title("Steps to Sweden")
st.sidebar.header("Useful Links")
st.sidebar.markdown("[GoFundMe Page](https://bit.ly/QUBStepsToSweden)")
st.sidebar.markdown("[Participant Sign-up Form](https://bit.ly/s2s-signup)")
st.sidebar.markdown("[Distance Log (Participants Only)](https://bit.ly/s2s-distance-log)")
st.sidebar.markdown("[Donation Log (Participants Only)](https://bit.ly/s2s-donation-log)")

# Main page
st.set_page_config(layout="centered")

####### UPDATE THESE VALUES #######
current_distance = 0  # km
current_donations = 0  # GBP
number_participants = 12
leaderboard_df = pd.read_csv("Tracker-2025-10-08.csv")

milestones = {
    "Belfast": "14th October",
    "Dublin": "",
    "Liverpool": "",
    "London": "",
    "Calais": "",
    "Antwerp": "",
    "Munster": "",
    "Hamburg": "",
    "Copenhagen": "",
    "Malmö": "",
    "Jönköping": "",
    "Stockholm": ""
    }

end_date = pd.to_datetime("2025-11-04")
start_date = pd.to_datetime("2025-10-14")

if pd.to_datetime("today") > start_date:
    days_remaining = (end_date - pd.to_datetime("today")).days
else:
    days_remaining = (end_date - start_date).days

image = Image.open("Form Banner.png")
st.image(image, width="content")

# st.title("Steps to Sweden")

gfm_url = "https://www.gofundme.com/f/qub-steps-to-sweden/widget/medium"

st.markdown(
    f"""
    <iframe src="{gfm_url}"
            width="100%"
            height="200"
            frameborder="0"
            scrolling="no">
    </iframe>
    """,
    unsafe_allow_html=True
)

distance_progress = st.container()
# donation_container = st.container()
# st.divider()
dist_calcs = st.container()
st.divider()
leaderboard_container = st.container()
top_calcs = st.container()
st.divider()
photo_gallery = st.container()

##########################################################################################################
# DISTANCE SECTION ###
with distance_progress:
    st.header("Distance Progress")

    col1, col2 = st.columns([3,1], vertical_alignment="center")

    with col1:
        image = Image.open("Dashboard - Map 1.png")
        st.image(image, width='content')   
    
    with col2:
        goal_distance = 2650  # km
        percent_complete = (current_distance / goal_distance) * 100

        st.metric(label="Goal (km):", value=f"{goal_distance}")
        st.metric(label="Travelled (km):", value=f"{current_distance}")
        st.metric(label="% of Goal Complete", value=f"{percent_complete:.1f}%")

    with st.expander("Click to view milestones"):

        st.subheader("📍 Milestones")

        # Show any progress, even if less than 1%
        progress_value = percent_complete / 100
        if 0 < progress_value < 0.01:
            st.progress(0.01)
        else:
            st.progress(min(progress_value, 1.0))

        for place, date in milestones.items():
            if date:  # If a date exists
                bg_color = "#6597C9"  # blue
                text_color = "white"
                display_text = f"{place} — {date}"
            else:     # No date yet
                bg_color = "#D3D3D3"  # grey
                text_color = "black"
                display_text = f"{place}"

            st.markdown(
                f"""
                <div style="
                    background-color:{bg_color};
                    color:{text_color};
                    padding:10px;
                    margin:5px 0;
                    border-radius:8px;
                    font-weight:bold;
                    text-align:center;
                ">
                    {display_text}
                </div>
                """,
                unsafe_allow_html=True
            )

##########################################################################################################
    
with dist_calcs:
    # Remaining distance
    dist_remaining = goal_distance - current_distance

    # Average distance needed per day
    avg_daily_dist = dist_remaining / days_remaining

    # Average distance per participant
    avg_per_person = avg_daily_dist / number_participants

    total_per_person = dist_remaining / number_participants

    metric1, metric2, metric3 = st.columns(3)
    metric1.metric("Days Remaining", f"{days_remaining}")
    metric2.metric("Distance Remaining", f"{dist_remaining} km")
    metric3.metric("Avg Distance per Day", f"{avg_daily_dist:.1f} km")

    with st.expander("Click to calculate distances per participant"):
        st.text(f"Number of Participants: {number_participants}")
        km1, km2 = st.columns(2)
        km1.metric("Total Distance Needed per Person", f"{total_per_person:.1f} km")
        km2.metric("Daily Distance Needed per Person", f"{avg_per_person:.1f} km")

        height_cm = st.number_input(
            "Enter your height (cm) to see this distance as steps:",
            min_value=100,
            max_value=250,
            value=170,  # default value
            step=1
        )

        stride_length_m = height_cm * 0.415 / 100
        steps_remaining = total_per_person * 1000 / stride_length_m
        avg_steps_per_day = steps_remaining / days_remaining

        step1, step2 = st.columns(2)
        step1.metric("Total Steps Needed", f"{steps_remaining:,.0f}")
        step2.metric("Avg Steps per Day", f"{avg_steps_per_day:,.0f}")


##########################################################################################################

## LEADERBOARD SECTION ###
with leaderboard_container:
    st.header("Distance Leaderboard")
    leader_df = leaderboard_df.sort_values(by="DISTANCE", ascending=False).reset_index(drop=True)
    leader_df["RANK"] = leader_df.index + 1

    # Create Plotly bar chart
    fig = px.bar(
        leader_df,
        x="DISTANCE",
        y="NAME",
        orientation='h',  # Horizontal bars
        text="DISTANCE",  # Show distance on each bar
        color="DISTANCE",
        color_continuous_scale="blugrn",
        height=400
    )

    # Polish layout
    fig.update_layout(
        yaxis=dict(autorange="reversed"),  # Highest value on top
        xaxis_title="Distance (km)",
        yaxis_title=" ",
        margin=dict(l=50, r=20, t=40, b=40),
        coloraxis_showscale=False  # Hide color legend
    )
    fig.update_traces(textposition='outside')

    # Display in Streamlit
    st.plotly_chart(fig, config={"responsive": True})

with top_calcs:
    with st.expander("Click for more details"):
        st.subheader("🏆 How Far to the Top?")
        # User selection
        selected_name = st.selectbox("Select your name:", leaderboard_df["NAME"])
        user_row = leader_df[leader_df["NAME"] == selected_name].iloc[0]
        user_distance = user_row["DISTANCE"]
        user_rank = user_row["RANK"]

        # Leader info
        leader_name = leader_df.iloc[0]["NAME"]
        leader_distance = leader_df.iloc[0]["DISTANCE"]

        # Estimate leader's daily pace so far
        # days_elapsed = (date.today() - start_date).days
        days_elapsed = 1
        leader_pace = leader_distance / days_elapsed

        # Predict where leader will be at the end
        leader_projected_total = leader_distance + (leader_pace * days_remaining)
        
        gap = max(0, leader_distance - user_distance)

        gap_to_projected_leader = leader_projected_total - user_distance
        daily_goal_dynamic = gap_to_projected_leader / days_remaining

        # Display results
        st.markdown(f"**{selected_name}**, you're currently in position #{user_rank} 🏅")
        st.metric("Your total distance", f"{user_distance:.1f} km")
        st.metric("Days left in challenge", f"{days_remaining} days")

        if user_rank == 1:
            st.success("You're in the lead! 🥇 Keep up the great work!")
        else:
            st.warning(f"You're {gap:.1f} km behind **{leader_name}** (top of the leaderboard) currently.")
            st.info(f"Assuming you and the leader both keep up your current paces, you will end up {gap_to_projected_leader}km behind. For you to reach the top by {end_date.strftime('%b %d')}, "
                    f"you’ll need to average **{daily_goal_dynamic:.1f} km/day**.")


    
##########################################################################################################
##### PHOTO SECTION #####
with photo_gallery:
    st.header("Photo Gallery")

    images = [
        "Photo1.png",
        "Photo2.png",
        "Photo3.png"
    ]
    captions = [
        "Caption for Photo 1",
        "Caption for Photo 2",
        "Caption for Photo 3"
    ]

    cols = st.columns(3)  # Adjust number of columns as needed

    for idx, (img_path, caption) in enumerate(zip(images, captions)):
        image = Image.open(img_path)
        cols[idx % 3].image(image, caption=caption, width='content')

date = pd.to_datetime("today").strftime("%d %B %Y %H:%M")
st.caption(f"Page last updated: {date}")