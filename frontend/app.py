import streamlit as st
import requests
from PIL import Image

st.title("VisionPilot AI")
st.subheader("Gemini Powered UI Navigator Agent")

goal = st.text_input("Enter Task", "Search laptop under 50000")
site_choice = st.selectbox(
    "Preferred Site",
    [
        "Auto",
        "Amazon India",
        "Amazon US",
        "Flipkart",
        "eBay",
        "Walmart",
        "Best Buy",
    ],
)

site_hints = {
    "Amazon India": "amazon.in",
    "Amazon US": "amazon.com",
    "Flipkart": "flipkart",
    "eBay": "ebay",
    "Walmart": "walmart",
    "Best Buy": "best buy",
}

if st.button("Run Agent"):

    st.write("Agent Running...")
    final_goal = goal
    if site_choice != "Auto":
        final_goal = f"{goal} on {site_hints[site_choice]}"

    try:
        response = requests.post(
            "http://127.0.0.1:8000/run-agent",
            json={"goal": final_goal},
            timeout=120,
        )
        response.raise_for_status()
        st.success(response.json())
    except requests.RequestException as exc:
        st.error(f"Backend request failed: {exc}")
    except ValueError:
        st.error("Backend returned a non-JSON response.")

try:
    img = Image.open("screen.png")
    st.image(img, caption="Latest Screenshot")
except FileNotFoundError:
    pass
except Exception as exc:
    st.warning(f"Could not load screenshot: {exc}")
