import streamlit as st
import requests
from PIL import Image

st.title("VisionPilot AI")
st.subheader("Gemini Powered Multi-Site Shopping Agent")

goal = st.text_input("Enter Task", "Search laptop under 50000")
site_choice = st.selectbox(
    "Preferred Site",
    [
        "Auto (Try Multiple Sites)",
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
    if site_choice in site_hints:
        final_goal = f"{goal} on {site_hints[site_choice]}"

    try:
        response = requests.post(
            "http://127.0.0.1:8000/run-agent",
            json={"goal": final_goal},
            timeout=120,
        )
        response.raise_for_status()
        payload = response.json()
        message = payload.get("message", "Completed")
        status = payload.get("status", "success")
        site = payload.get("site", "Auto")
        results = payload.get("results") or []
        optimal_result = payload.get("optimal_result") or {}
        fx_source = payload.get("fx_source")

        if status == "error":
            st.error(message)
        elif status == "partial":
            st.warning(message)
        else:
            st.success(message)

        st.caption(f"Target: {site}")
        if fx_source:
            st.caption(f"FX source: {fx_source}")
        if optimal_result:
            best_title = optimal_result.get("title") or "Untitled"
            best_price = optimal_result.get("price") or "N/A"
            best_site = optimal_result.get("site") or "Unknown"
            best_url = optimal_result.get("url") or ""
            best_currency = optimal_result.get("currency") or "UNKNOWN"
            best_inr = optimal_result.get("normalized_price_inr")
            st.markdown("### Best Ranked Result")
            st.markdown(f"**{best_title}**")
            st.caption(f"Site: {best_site}")
            st.write(f"Price: {best_price} ({best_currency})")
            if best_inr is not None:
                st.write(f"Normalized (INR): ₹{best_inr}")
            if best_url:
                st.markdown(f"[Open Best Product]({best_url})")
            st.divider()

        if results:
            st.markdown("### Top Results")
            for idx, item in enumerate(results, start=1):
                title = item.get("title") or "Untitled"
                price = item.get("price") or "N/A"
                url = item.get("url") or ""
                source_site = item.get("site") or site
                currency = item.get("currency") or "UNKNOWN"
                normalized_price = item.get("normalized_price_inr")
                st.markdown(f"**{idx}. {title}**")
                st.caption(f"Site: {source_site}")
                st.write(f"Price: {price} ({currency})")
                if normalized_price is not None:
                    st.caption(f"Normalized (INR): ₹{normalized_price}")
                if url:
                    st.markdown(f"[Open Product]({url})")
                st.divider()
        else:
            st.info("No products were extracted. Try a more specific query.")
    except requests.RequestException as exc:
        error_message = str(exc)
        resp = getattr(exc, "response", None)
        if resp is not None:
            try:
                detail = resp.json().get("detail")
                if detail:
                    error_message = f"{error_message} | detail: {detail}"
            except ValueError:
                pass
        st.error(f"Backend request failed: {error_message}")
    except ValueError:
        st.error("Backend returned a non-JSON response.")

try:
    img = Image.open("screen.png")
    st.image(img, caption="Latest Screenshot")
except FileNotFoundError:
    pass
except Exception as exc:
    st.warning(f"Could not load screenshot: {exc}")
