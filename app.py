# movie_booking_app.py
import streamlit as st
import pandas as pd
import numpy as np
import datetime
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import json
from PIL import Image
import io

# Set page configuration
st.set_page_config(
    page_title="CineMagic - Movie Ticket Booking",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced UI
st.markdown("""
<style>
    /* Main Theme */
    :root {
        --primary: #0f172a;
        --secondary: #1e293b;
        --accent: #3b82f6;
        --accent-light: #60a5fa;
        --text: #f8fafc;
        --text-secondary: #94a3b8;
        --success: #10b981;
        --warning: #f59e0b;
        --danger: #ef4444;
    }
    
    .main {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
        color: var(--text);
    }
    
    /* Headers */
    .main-header {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(90deg, #3b82f6, #8b5cf6, #ec4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem;
        margin-bottom: 2rem;
        text-shadow: 0 2px 10px rgba(59, 130, 246, 0.3);
    }
    
    .section-header {
        font-size: 1.8rem;
        font-weight: 700;
        color: var(--text);
        margin: 1.5rem 0;
        padding-left: 0.5rem;
        border-left: 4px solid var(--accent);
    }
    
    /* Cards */
    .movie-card {
        background: linear-gradient(145deg, #1e293b, #0f172a);
        border-radius: 16px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .movie-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #3b82f6, #8b5cf6);
    }
    
    .movie-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(59, 130, 246, 0.2);
        border-color: rgba(59, 130, 246, 0.3);
    }
    
    .theater-card {
        background: linear-gradient(135deg, #1e293b, #334155);
        border-radius: 12px;
        padding: 15px;
        margin: 10px 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.2s ease;
    }
    
    .theater-card:hover {
        border-color: var(--accent);
        background: linear-gradient(135deg, #334155, #475569);
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(90deg, var(--accent), var(--accent-light));
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 8px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4);
    }
    
    .secondary-btn {
        background: linear-gradient(90deg, #475569, #64748b) !important;
    }
    
    /* Progress bars and indicators */
    .progress-bar {
        height: 8px;
        background: linear-gradient(90deg, #3b82f6, #8b5cf6);
        border-radius: 4px;
        margin: 10px 0;
    }
    
    /* Badges */
    .badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin: 0 5px 5px 0;
    }
    
    .badge-premium {
        background: linear-gradient(90deg, #f59e0b, #fbbf24);
        color: #1e293b;
    }
    
    .badge-imax {
        background: linear-gradient(90deg, #8b5cf6, #a78bfa);
        color: white;
    }
    
    .badge-3d {
        background: linear-gradient(90deg, #10b981, #34d399);
        color: white;
    }
    
    /* Seats */
    .seat-available {
        background: linear-gradient(135deg, #10b981, #34d399);
        color: white;
    }
    
    .seat-selected {
        background: linear-gradient(135deg, #3b82f6, #60a5fa);
        color: white;
        animation: pulse 2s infinite;
    }
    
    .seat-booked {
        background: linear-gradient(135deg, #64748b, #94a3b8);
        color: white;
        cursor: not-allowed;
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(59, 130, 246, 0.7); }
        70% { box-shadow: 0 0 0 10px rgba(59, 130, 246, 0); }
        100% { box-shadow: 0 0 0 0 rgba(59, 130, 246, 0); }
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
        background-color: var(--secondary);
        border-radius: 8px;
        padding: 4px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 6px;
        padding: 10px 20px;
        background-color: transparent;
        color: var(--text-secondary);
    }
    
    .stTabs [aria-selected="true"] {
        background-color: var(--accent) !important;
        color: white !important;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
    }
    
    /* Inputs */
    .stTextInput>div>div>input, 
    .stSelectbox>div>div>select,
    .stDateInput>div>div>input {
        background-color: #1e293b !important;
        color: white !important;
        border: 1px solid #475569 !important;
        border-radius: 8px !important;
    }
    
    /* Movie poster hover effect */
    .poster-container {
        position: relative;
        overflow: hidden;
        border-radius: 12px;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4);
    }
    
    .poster-container img {
        transition: transform 0.5s ease;
    }
    
    .poster-container:hover img {
        transform: scale(1.05);
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1e293b;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #3b82f6, #8b5cf6);
        border-radius: 5px;
    }
    
    /* Stats cards */
    .stat-card {
        background: linear-gradient(135deg, #1e293b, #334155);
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .stat-value {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(90deg, #3b82f6, #8b5cf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Confetti effect container */
    .confetti-container {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 1000;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    if 'bookings' not in st.session_state:
        st.session_state.bookings = []
    if 'user_info' not in st.session_state:
        st.session_state.user_info = {}
    if 'selected_seats' not in st.session_state:
        st.session_state.selected_seats = []
    if 'cart' not in st.session_state:
        st.session_state.cart = []
    if 'show_confetti' not in st.session_state:
        st.session_state.show_confetti = False
    if 'current_movie' not in st.session_state:
        st.session_state.current_movie = None
    if 'current_theater' not in st.session_state:
        st.session_state.current_theater = None

init_session_state()

# Sample movie data with enhanced details
def generate_movie_data():
    movies = [
        {
            "id": 1,
            "title": "The Quantum Paradox",
            "genre": ["Sci-Fi", "Action", "Thriller"],
            "duration": "2h 28m",
            "rating": 8.7,
            "imdb_rating": 8.5,
            "release_date": datetime.now() - timedelta(days=15),
            "poster_color": "#3b82f6",
            "description": "A scientist discovers a way to travel between parallel dimensions, but soon realizes each jump alters reality.",
            "director": "Christopher Nolan",
            "cast": ["Leonardo DiCaprio", "Emily Blunt", "Michael B. Jordan"],
            "languages": ["English", "IMAX", "3D"],
            "age_rating": "PG-13",
            "trailer_url": "https://youtube.com/watch?v=example1"
        },
        {
            "id": 2,
            "title": "Midnight in Paris",
            "genre": ["Romance", "Drama", "Fantasy"],
            "duration": "1h 34m",
            "rating": 7.9,
            "imdb_rating": 7.7,
            "release_date": datetime.now() - timedelta(days=30),
            "poster_color": "#8b5cf6",
            "description": "A writer finds himself mysteriously transported to 1920s Paris every night at midnight.",
            "director": "Woody Allen",
            "cast": ["Owen Wilson", "Rachel McAdams", "Marion Cotillard"],
            "languages": ["English", "French"],
            "age_rating": "PG",
            "trailer_url": "https://youtube.com/watch?v=example2"
        },
        {
            "id": 3,
            "title": "The Last Samurai",
            "genre": ["Action", "Drama", "History"],
            "duration": "2h 34m",
            "rating": 8.3,
            "imdb_rating": 8.1,
            "release_date": datetime.now() - timedelta(days=45),
            "poster_color": "#ef4444",
            "description": "An American military advisor embraces the Samurai culture he was hired to destroy.",
            "director": "Edward Zwick",
            "cast": ["Tom Cruise", "Ken Watanabe", "Billy Connolly"],
            "languages": ["English", "Japanese", "IMAX"],
            "age_rating": "R",
            "trailer_url": "https://youtube.com/watch?v=example3"
        },
        {
            "id": 4,
            "title": "Cosmic Dreams",
            "genre": ["Animation", "Adventure", "Family"],
            "duration": "1h 42m",
            "rating": 8.9,
            "imdb_rating": 8.7,
            "release_date": datetime.now() - timedelta(days=5),
            "poster_color": "#10b981",
            "description": "A young astronaut embarks on a journey through the solar system to rescue her scientist father.",
            "director": "Pete Docter",
            "cast": ["Saoirse Ronan", "Chris Pratt", "Zendaya"],
            "languages": ["English", "3D", "IMAX 3D"],
            "age_rating": "G",
            "trailer_url": "https://youtube.com/watch?v=example4"
        },
        {
            "id": 5,
            "title": "Neon Nights",
            "genre": ["Crime", "Thriller", "Mystery"],
            "duration": "2h 15m",
            "rating": 8.1,
            "imdb_rating": 7.9,
            "release_date": datetime.now() - timedelta(days=60),
            "poster_color": "#f59e0b",
            "description": "A detective investigates a series of mysterious deaths in a futuristic cyberpunk city.",
            "director": "Denis Villeneuve",
            "cast": ["Ryan Gosling", "Ana de Armas", "Harrison Ford"],
            "languages": ["English", "Dolby Atmos"],
            "age_rating": "R",
            "trailer_url": "https://youtube.com/watch?v=example5"
        }
    ]
    return movies

# Theater data
def generate_theater_data():
    theaters = [
        {
            "id": 1,
            "name": "IMAX Megaplex",
            "location": "Downtown Entertainment District",
            "screens": ["IMAX", "4DX", "Dolby Cinema"],
            "amenities": ["Recliner Seats", "Dolby Atmos", "Gourmet Food", "Bar"],
            "distance": "1.2 miles"
        },
        {
            "id": 2,
            "name": "Royal Cinemas",
            "location": "Westgate Mall",
            "screens": ["Premium Lounger", "3D", "Standard"],
            "amenities": ["Luxury Loungers", "In-seat Service", "VIP Lounge"],
            "distance": "3.5 miles"
        },
        {
            "id": 3,
            "name": "Starlight Drive-In",
            "location": "Northside Highway",
            "screens": ["Drive-In", "Open Air"],
            "amenities": ["Car Service", "Retro Snacks", "Family Zone"],
            "distance": "5.8 miles"
        },
        {
            "id": 4,
            "name": "CineMagic Premium",
            "location": "Riverfront Plaza",
            "screens": ["IMAX", "ScreenX", "4DX", "Dolby Vision"],
            "amenities": ["Butler Service", "Fine Dining", "Wine Bar", "Valet Parking"],
            "distance": "2.1 miles"
        }
    ]
    return theaters

# Generate showtimes
def generate_showtimes(movie_id, theater_id):
    showtimes = []
    base_time = datetime.now().replace(hour=10, minute=0, second=0, microsecond=0)
    
    formats = ["2D", "3D", "IMAX", "4DX", "Dolby Atmos"]
    prices = {
        "2D": 12.99,
        "3D": 16.99,
        "IMAX": 19.99,
        "4DX": 24.99,
        "Dolby Atmos": 22.99
    }
    
    for i in range(5):  # 5 days
        for j in range(6):  # 6 shows per day
            show_time = base_time + timedelta(days=i, hours=j*3)
            format_type = random.choice(formats)
            
            showtimes.append({
                "id": len(showtimes) + 1,
                "movie_id": movie_id,
                "theater_id": theater_id,
                "time": show_time,
                "format": format_type,
                "price": prices[format_type],
                "available_seats": random.randint(20, 150)
            })
    
    return showtimes

# Generate seat layout
def generate_seat_layout(rows=10, cols=12):
    seats = []
    seat_types = ['available', 'available', 'available', 'booked']
    
    for row in range(rows):
        for col in range(cols):
            if col == 5 or col == 6:  # Leave aisle
                continue
            
            seat_type = random.choice(seat_types)
            price_multiplier = 1.0
            if row < 3:  # Premium seats
                seat_type = 'available'
                price_multiplier = 1.5
            
            seats.append({
                "id": f"{chr(65+row)}{col+1}",
                "row": chr(65 + row),
                "number": col + 1,
                "type": seat_type,
                "price_multiplier": price_multiplier,
                "x": col,
                "y": row
            })
    
    return seats

# Navigation sidebar
def navigation():
    st.sidebar.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <h1 style="font-size: 2.5rem; margin: 0;">🎬</h1>
        <h2 style="margin: 0; color: #60a5fa;">CineMagic</h2>
        <p style="color: #94a3b8; font-size: 0.9rem;">Premium Movie Experience</p>
    </div>
    """, unsafe_allow_html=True)
    
    page = st.sidebar.radio(
        "Navigate",
        ["🎥 Home", "📽️ Movies", "🎟️ Book Tickets", "🎭 Theaters", "📊 Analytics", "🛒 Cart", "👤 Profile"],
        label_visibility="collapsed"
    )
    
    st.sidebar.markdown("---")
    
    # Quick stats
    st.sidebar.markdown("""
    <div class="stat-card">
        <div class="stat-value">{}</div>
        <div style="color: #94a3b8;">Movies Showing</div>
    </div>
    """.format(len(generate_movie_data())), unsafe_allow_html=True)
    
    st.sidebar.markdown("""
    <div class="stat-card">
        <div class="stat-value">{}</div>
        <div style="color: #94a3b8;">Premium Theaters</div>
    </div>
    """.format(len(generate_theater_data())), unsafe_allow_html=True)
    
    return page

# Home Page
def home_page():
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.markdown('<h1 class="main-header">🎬 CineMagic</h1>', unsafe_allow_html=True)
        st.markdown('<p style="text-align: center; color: #94a3b8; font-size: 1.2rem;">Experience Cinema Like Never Before</p>', unsafe_allow_html=True)
    
    # Hero Section
    st.markdown("---")
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown('<h2 class="section-header">🎞️ Now Showing</h2>', unsafe_allow_html=True)
        
        movies = generate_movie_data()
        
        # Featured movie carousel
        featured_movie = movies[0]
        
        st.markdown(f"""
        <div class="movie-card">
            <div style="display: flex; gap: 20px;">
                <div style="flex: 1;">
                    <h3 style="margin: 0 0 10px 0; font-size: 1.8rem;">{featured_movie['title']}</h3>
                    <div style="display: flex; gap: 10px; margin-bottom: 15px;">
                        <span class="badge badge-premium">IMAX</span>
                        <span class="badge badge-3d">3D</span>
                        <span style="color: #fbbf24;">{'⭐' * int(featured_movie['rating'])}</span>
                        <span style="color: #94a3b8;">{featured_movie['rating']}/10</span>
                    </div>
                    <p style="color: #cbd5e1; line-height: 1.6;">{featured_movie['description']}</p>
                    <div style="margin-top: 20px;">
                        <p><strong>Director:</strong> {featured_movie['director']}</p>
                        <p><strong>Cast:</strong> {', '.join(featured_movie['cast'][:3])}</p>
                        <p><strong>Duration:</strong> {featured_movie['duration']} • <strong>Rating:</strong> {featured_movie['age_rating']}</p>
                    </div>
                </div>
                <div style="width: 150px;">
                    <div class="poster-container">
                        <div style="width: 150px; height: 225px; background: linear-gradient(135deg, {featured_movie['poster_color']}, #1e293b); 
                                border-radius: 12px; display: flex; align-items: center; justify-content: center;">
                            <span style="font-size: 3rem;">🎬</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown('<h2 class="section-header">⏰ Quick Book</h2>', unsafe_allow_html=True)
        
        with st.form("quick_booking"):
            movie = st.selectbox("Select Movie", [m['title'] for m in movies])
            theater = st.selectbox("Select Theater", ["IMAX Megaplex", "Royal Cinemas", "Starlight Drive-In", "CineMagic Premium"])
            date = st.date_input("Date", datetime.now())
            time = st.selectbox("Time", ["10:00 AM", "1:30 PM", "4:00 PM", "7:00 PM", "10:30 PM"])
            tickets = st.slider("Tickets", 1, 10, 2)
            
            if st.form_submit_button("🎟️ Find Seats", use_container_width=True):
                st.session_state.page = "🎟️ Book Tickets"
                st.rerun()
        
        # Special offers
        st.markdown("""
        <div class="movie-card" style="margin-top: 20px;">
            <h4 style="margin: 0 0 10px 0;">🎁 Special Offers</h4>
            <p style="color: #94a3b8; font-size: 0.9rem;">• 20% off on Wednesdays</p>
            <p style="color: #94a3b8; font-size: 0.9rem;">• Buy 1 Get 1 Free before 12 PM</p>
            <p style="color: #94a3b8; font-size: 0.9rem;">• Student discount available</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Now Showing Grid
    st.markdown('<h2 class="section-header">🎭 All Movies</h2>', unsafe_allow_html=True)
    
    movies = generate_movie_data()
    cols = st.columns(5)
    
    for idx, movie in enumerate(movies):
        with cols[idx % 5]:
            st.markdown(f"""
            <div class="movie-card" style="text-align: center; cursor: pointer;" onclick="this.style.transform='scale(1.02)'">
                <div class="poster-container">
                    <div style="width: 100%; height: 200px; background: linear-gradient(135deg, {movie['poster_color']}, #1e293b); 
                            border-radius: 12px; display: flex; align-items: center; justify-content: center; margin-bottom: 15px;">
                        <span style="font-size: 2.5rem;">🎬</span>
                    </div>
                </div>
                <h4 style="margin: 10px 0 5px 0;">{movie['title']}</h4>
                <div style="display: flex; justify-content: center; gap: 5px; margin-bottom: 10px;">
                    {'⭐' * int(movie['rating'])}
                </div>
                <p style="color: #94a3b8; font-size: 0.9rem; margin: 0;">{movie['duration']} • {movie['age_rating']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Book Now", key=f"book_{movie['id']}", use_container_width=True):
                st.session_state.current_movie = movie
                st.session_state.page = "🎟️ Book Tickets"
                st.rerun()

# Movies Page
def movies_page():
    st.markdown('<h1 class="main-header">🎥 Browse Movies</h1>', unsafe_allow_html=True)
    
    # Filters
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        genre = st.multiselect("Genre", ["Action", "Comedy", "Drama", "Sci-Fi", "Thriller", "Romance", "Horror", "Animation"])
    
    with col2:
        language = st.multiselect("Format", ["IMAX", "3D", "4DX", "Dolby Atmos", "2D"])
    
    with col3:
        rating = st.slider("Minimum Rating", 0.0, 10.0, 7.0, 0.5)
    
    with col4:
        sort_by = st.selectbox("Sort By", ["Popular", "Newest", "Rating", "Duration"])
    
    # Movies grid
    movies = generate_movie_data()
    
    for movie in movies:
        if genre and not any(g in movie['genre'] for g in genre):
            continue
        if rating > movie['rating']:
            continue
        
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.markdown(f"""
            <div class="poster-container">
                <div style="width: 100%; height: 250px; background: linear-gradient(135deg, {movie['poster_color']}, #1e293b); 
                        border-radius: 12px; display: flex; align-items: center; justify-content: center;">
                    <span style="font-size: 4rem;">🎬</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="movie-card">
                <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                    <div>
                        <h3 style="margin: 0 0 10px 0; font-size: 1.8rem;">{movie['title']}</h3>
                        <div style="display: flex; gap: 10px; margin-bottom: 15px;">
                            {''.join([f'<span class="badge" style="background: {movie["poster_color"]}30; color: {movie["poster_color"]};">{g}</span>' for g in movie['genre'][:2]])}
                            <span class="badge badge-premium">IMAX</span>
                            <span style="color: #fbbf24;">{'⭐' * int(movie['rating'])} {movie['rating']}</span>
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <h3 style="color: #60a5fa; margin: 0;">From $12.99</h3>
                        <p style="color: #94a3b8; margin: 5px 0;">{movie['duration']}</p>
                    </div>
                </div>
                
                <p style="color: #cbd5e1; line-height: 1.6; margin: 15px 0;">{movie['description']}</p>
                
                <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 20px;">
                    <div>
                        <p style="color: #94a3b8; margin: 0; font-size: 0.9rem;">
                            <strong>Director:</strong> {movie['director']} • 
                            <strong>Cast:</strong> {', '.join(movie['cast'][:2])}
                        </p>
                    </div>
                    <div>
                        <button onclick="alert('Booking {movie["title"]}')" style="background: linear-gradient(90deg, {movie['poster_color']}, #60a5fa); 
                                color: white; border: none; padding: 10px 20px; border-radius: 6px; cursor: pointer; font-weight: 600;">
                            Book Tickets
                        </button>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# Booking Page
def booking_page():
    st.markdown('<h1 class="main-header">🎟️ Book Tickets</h1>', unsafe_allow_html=True)
    
    # Step indicator
    steps = ["Select Movie", "Choose Theater", "Pick Seats", "Confirm Booking"]
    current_step = 3
    
    col1, col2, col3, col4 = st.columns(4)
    for i, step in enumerate(steps):
        col = col1 if i == 0 else col2 if i == 1 else col3 if i == 2 else col4
        with col:
            is_active = i < current_step
            is_current = i == current_step - 1
            
            st.markdown(f"""
            <div style="text-align: center; padding: 10px; border-radius: 8px; 
                        background: {'linear-gradient(90deg, #3b82f6, #60a5fa)' if is_current else '#1e293b' if is_active else '#0f172a'};
                        border: 1px solid {'#3b82f6' if is_current or is_active else '#475569'};">
                <div style="width: 30px; height: 30px; border-radius: 50%; background: white; color: #0f172a; 
                            display: flex; align-items: center; justify-content: center; margin: 0 auto 10px auto; font-weight: bold;">
                    {i + 1}
                </div>
                <div style="color: white; font-weight: {'600' if is_current or is_active else '400'};">{step}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Seat selection
    st.markdown('<h2 class="section-header">🎭 Select Your Seats</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        # Seat layout
        st.markdown("""
        <div style="background: #0f172a; padding: 20px; border-radius: 12px; border: 1px solid #334155;">
            <div style="text-align: center; margin-bottom: 30px;">
                <div style="width: 80%; height: 20px; background: linear-gradient(90deg, #475569, #64748b); 
                        margin: 0 auto 40px auto; border-radius: 4px;"></div>
                <h3 style="color: #94a3b8;">SCREEN</h3>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Generate seat grid
        rows = 8
        cols = 12
        
        seat_layout = ""
        for row in range(rows):
            row_label = chr(65 + row)
            seat_row = f"<div style='display: flex; align-items: center; margin: 10px 0;'>"
            seat_row += f"<div style='width: 40px; color: #94a3b8; font-weight: bold;'>{row_label}</div>"
            
            for col in range(1, cols + 1):
                if col == 6:
                    seat_row += "<div style='width: 40px;'></div>"  # Aisle
                
                seat_id = f"{row_label}{col}"
                seat_type = "available"
                if random.random() < 0.3:  # 30% booked
                    seat_type = "booked"
                
                if seat_id in st.session_state.selected_seats:
                    seat_type = "selected"
                
                seat_row += f"""
                <div class='seat-{seat_type}' style='
                    width: 30px; height: 30px; margin: 0 5px; border-radius: 6px;
                    display: flex; align-items: center; justify-content: center;
                    cursor: {"" if seat_type != "booked" else "not-allowed"};
                    background: {"#10b981" if seat_type == "available" else "#3b82f6" if seat_type == "selected" else "#64748b"};
                    color: white; font-weight: bold; font-size: 0.8rem;'
                    onclick="if(this.style.background != 'rgb(100, 116, 139)') {{
                        this.style.background = this.style.background == 'rgb(59, 130, 246)' ? '#10b981' : '#3b82f6';
                        this.classList.toggle('seat-selected');
                    }}">
                    {col}
                </div>
                """
            
            seat_row += "</div>"
            seat_layout += seat_row
        
        st.markdown(f"""
        <div style="background: #0f172a; padding: 20px; border-radius: 12px; border: 1px solid #334155; margin-top: 20px;">
            {seat_layout}
        </div>
        """, unsafe_allow_html=True)
        
        # Seat legend
        st.markdown("""
        <div style="display: flex; justify-content: center; gap: 20px; margin-top: 20px;">
            <div style="display: flex; align-items: center; gap: 5px;">
                <div style="width: 20px; height: 20px; background: #10b981; border-radius: 4px;"></div>
                <span style="color: #94a3b8;">Available</span>
            </div>
            <div style="display: flex; align-items: center; gap: 5px;">
                <div style="width: 20px; height: 20px; background: #3b82f6; border-radius: 4px;"></div>
                <span style="color: #94a3b8;">Selected</span>
            </div>
            <div style="display: flex; align-items: center; gap: 5px;">
                <div style="width: 20px; height: 20px; background: #64748b; border-radius: 4px;"></div>
                <span style="color: #94a3b8;">Booked</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Booking summary
        selected_movie = st.session_state.current_movie or generate_movie_data()[0]
        
        st.markdown(f"""
        <div class="movie-card">
            <div style="display: flex; gap: 15px; margin-bottom: 20px;">
                <div style="width: 80px; height: 120px; background: linear-gradient(135deg, {selected_movie['poster_color']}, #1e293b); 
                        border-radius: 8px; display: flex; align-items: center; justify-content: center;">
                    <span style="font-size: 2rem;">🎬</span>
                </div>
                <div>
                    <h3 style="margin: 0 0 5px 0;">{selected_movie['title']}</h3>
                    <p style="color: #94a3b8; margin: 0 0 10px 0;">IMAX • 3D</p>
                    <div style="display: flex; gap: 5px;">
                        {'⭐' * int(selected_movie['rating'])}
                    </div>
                </div>
            </div>
            
            <div style="background: #0f172a; padding: 15px; border-radius: 8px; margin: 15px 0;">
                <p style="margin: 0 0 10px 0; color: #94a3b8;">🎭 <strong>IMAX Megaplex</strong></p>
                <p style="margin: 0 0 10px 0; color: #94a3b8;">📅 <strong>Today</strong> | 🕒 <strong>7:00 PM</strong></p>
                <p style="margin: 0; color: #94a3b8;">💺 <strong>Seats:</strong> {', '.join(st.session_state.selected_seats) if st.session_state.selected_seats else 'Not selected'}</p>
            </div>
            
            <div style="margin: 20px 0;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                    <span style="color: #94a3b8;">Tickets (2x)</span>
                    <span style="color: white; font-weight: bold;">$39.98</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                    <span style="color: #94a3b8;">Premium Seats</span>
                    <span style="color: white; font-weight: bold;">$10.00</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                    <span style="color: #94a3b8;">Service Fee</span>
                    <span style="color: white; font-weight: bold;">$3.99</span>
                </div>
                <div style="height: 1px; background: #334155; margin: 15px 0;"></div>
                <div style="display: flex; justify-content: space-between;">
                    <span style="color: white; font-size: 1.2rem; font-weight: bold;">Total</span>
                    <span style="color: #60a5fa; font-size: 1.5rem; font-weight: bold;">$53.97</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Promo code
        with st.expander("💳 Apply Promo Code"):
            promo_code = st.text_input("Enter promo code")
            if st.button("Apply", use_container_width=True):
                st.success("Promo code applied! $5 discount added.")
        
        # Payment button
        if st.button("🎟️ Proceed to Payment", use_container_width=True):
            st.session_state.show_confetti = True
            st.success("Booking confirmed! Check your email for tickets.")
            st.balloons()
            
            # Add to bookings
            booking = {
                "id": f"BK{random.randint(100000, 999999)}",
                "movie": selected_movie,
                "theater": "IMAX Megaplex",
                "showtime": "7:00 PM",
                "seats": st.session_state.selected_seats,
                "total": 53.97,
                "date": datetime.now(),
                "status": "Confirmed"
            }
            st.session_state.bookings.append(booking)
            
            # Clear selected seats
            st.session_state.selected_seats = []

# Theaters Page
def theaters_page():
    st.markdown('<h1 class="main-header">🎭 Premium Theaters</h1>', unsafe_allow_html=True)
    
    theaters = generate_theater_data()
    
    for theater in theaters:
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.markdown(f"""
            <div style="width: 100%; height: 200px; background: linear-gradient(135deg, #1e293b, #334155); 
                    border-radius: 12px; display: flex; align-items: center; justify-content: center;">
                <span style="font-size: 3rem;">🎦</span>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="theater-card">
                <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                    <div>
                        <h3 style="margin: 0 0 10px 0; font-size: 1.5rem;">{theater['name']}</h3>
                        <p style="color: #94a3b8; margin: 0 0 15px 0;">📍 {theater['location']}</p>
                        <div style="display: flex; gap: 10px; margin-bottom: 15px;">
                            {''.join([f'<span class="badge" style="background: #3b82f630; color: #60a5fa;">{s}</span>' for s in theater['screens'][:3]])}
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <div style="color: #60a5fa; font-weight: bold; font-size: 1.2rem;">{theater['distance']}</div>
                        <p style="color: #94a3b8; margin: 5px 0 0 0;">away</p>
                    </div>
                </div>
                
                <div style="margin-top: 15px;">
                    <p style="color: #94a3b8; margin: 0 0 10px 0; font-size: 0.9rem;">
                        <strong>Amenities:</strong> {', '.join(theater['amenities'][:3])}
                    </p>
                    <div style="display: flex; gap: 10px;">
                        <button style="background: linear-gradient(90deg, #3b82f6, #60a5fa); color: white; 
                                border: none; padding: 8px 16px; border-radius: 6px; cursor: pointer; font-weight: 600;">
                            View Showtimes
                        </button>
                        <button style="background: transparent; color: #60a5fa; border: 1px solid #60a5fa; 
                                padding: 8px 16px; border-radius: 6px; cursor: pointer; font-weight: 600;">
                            Get Directions
                        </button>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# Analytics Page
def analytics_page():
    st.markdown('<h1 class="main-header">📊 Movie Analytics</h1>', unsafe_allow_html=True)
    
    # Stats cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-value">2,847</div>
            <div style="color: #94a3b8;">Tickets Sold Today</div>
            <div style="color: #10b981; font-size: 0.9rem; margin-top: 5px;">↑ 12% from yesterday</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-value">$42.8K</div>
            <div style="color: #94a3b8;">Revenue Today</div>
            <div style="color: #10b981; font-size: 0.9rem; margin-top: 5px;">↑ 8% from yesterday</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-value">78%</div>
            <div style="color: #94a3b8;">Occupancy Rate</div>
            <div style="color: #f59e0b; font-size: 0.9rem; margin-top: 5px;">↓ 2% from last week</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-value">4.7</div>
            <div style="color: #94a3b8;">Avg. Customer Rating</div>
            <div style="color: #10b981; font-size: 0.9rem; margin-top: 5px;">↑ 0.3 this month</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Genre distribution
        genres = ["Action", "Comedy", "Drama", "Sci-Fi", "Thriller", "Romance"]
        values = [25, 18, 22, 15, 12, 8]
        
        fig = go.Figure(data=[go.Pie(labels=genres, values=values, hole=.3,
                                   marker=dict(colors=['#3b82f6', '#8b5cf6', '#10b981', '#f59e0b', '#ef4444', '#ec4899']))])
        fig.update_layout(title_text="🎭 Movie Genre Distribution", 
                         template="plotly_dark",
                         height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Revenue trend
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        revenue = [32000, 28500, 31200, 42800, 51200, 68500, 72300]
        
        fig = go.Figure(data=[go.Bar(x=days, y=revenue,
                                   marker_color='#3b82f6',
                                   text=[f'${r/1000:.1f}K' for r in revenue],
                                   textposition='auto')])
        fig.update_layout(title_text="💰 Weekly Revenue Trend",
                         template="plotly_dark",
                         height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Top movies
    st.markdown('<h2 class="section-header">🏆 Top Performing Movies</h2>', unsafe_allow_html=True)
    
    movies = generate_movie_data()
    top_movies = sorted(movies, key=lambda x: x['rating'], reverse=True)[:3]
    
    cols = st.columns(3)
    for idx, movie in enumerate(top_movies):
        with cols[idx]:
            st.markdown(f"""
            <div class="movie-card" style="text-align: center;">
                <div style="position: relative;">
                    <div style="width: 100%; height: 180px; background: linear-gradient(135deg, {movie['poster_color']}, #1e293b); 
                            border-radius: 12px; display: flex; align-items: center; justify-content: center; margin-bottom: 15px;">
                        <span style="font-size: 3rem;">🎬</span>
                    </div>
                    <div style="position: absolute; top: 10px; right: 10px; background: #f59e0b; color: #1e293b; 
                            padding: 5px 10px; border-radius: 20px; font-weight: bold; font-size: 0.8rem;">
                        #{idx + 1}
                    </div>
                </div>
                <h4 style="margin: 10px 0 5px 0;">{movie['title']}</h4>
                <div style="display: flex; justify-content: center; gap: 5px; margin-bottom: 10px;">
                    {'⭐' * int(movie['rating'])}
                    <span style="color: #fbbf24;">{movie['rating']}</span>
                </div>
                <p style="color: #94a3b8; font-size: 0.9rem; margin: 0;">Revenue: ${random.randint(5, 15)}M</p>
                <p style="color: #94a3b8; font-size: 0.9rem; margin: 0;">Tickets: {random.randint(1000, 5000)}K</p>
            </div>
            """, unsafe_allow_html=True)

# Cart Page
def cart_page():
    st.markdown('<h1 class="main-header">🛒 Your Cart</h1>', unsafe_allow_html=True)
    
    if not st.session_state.get('cart'):
        st.info("🛍️ Your cart is empty! Browse movies and add some tickets.")
        return
    
    # Cart items
    total = 0
    for idx, item in enumerate(st.session_state.cart):
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            st.markdown(f"""
            <div class="movie-card">
                <div style="display: flex; gap: 15px;">
                    <div style="width: 80px; height: 120px; background: linear-gradient(135deg, {item['poster_color']}, #1e293b); 
                            border-radius: 8px; display: flex; align-items: center; justify-content: center;">
                        <span style="font-size: 2rem;">🎬</span>
                    </div>
                    <div style="flex: 1;">
                        <h4 style="margin: 0 0 5px 0;">{item['title']}</h4>
                        <p style="color: #94a3b8; margin: 0 0 10px 0;">{item['theater']} • {item['showtime']}</p>
                        <p style="color: #94a3b8; margin: 0;">{item['tickets']} tickets • {item['seats']}</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="text-align: center; padding: 20px;">
                <h3 style="color: #60a5fa; margin: 0;">${item['price']}</h3>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            if st.button("❌ Remove", key=f"remove_{idx}"):
                st.session_state.cart.pop(idx)
                st.rerun()
        
        total += item['price']
    
    st.markdown("---")
    
    # Checkout
    col1, col2 = st.columns([2, 1])
    
    with col2:
        st.markdown(f"""
        <div class="movie-card">
            <h4 style="margin: 0 0 20px 0;">Order Summary</h4>
            <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                <span style="color: #94a3b8;">Subtotal</span>
                <span style="color: white; font-weight: bold;">${total:.2f}</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                <span style="color: #94a3b8;">Service Fee</span>
                <span style="color: white; font-weight: bold;">${total * 0.1:.2f}</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                <span style="color: #94a3b8;">Tax</span>
                <span style="color: white; font-weight: bold;">${total * 0.08:.2f}</span>
            </div>
            <div style="height: 1px; background: #334155; margin: 15px 0;"></div>
            <div style="display: flex; justify-content: space-between;">
                <span style="color: white; font-size: 1.2rem; font-weight: bold;">Total</span>
                <span style="color: #60a5fa; font-size: 1.5rem; font-weight: bold;">${total * 1.18:.2f}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("💳 Proceed to Checkout", use_container_width=True):
            st.success("Order placed successfully!")
            st.session_state.cart = []

# Profile Page
def profile_page():
    st.markdown('<h1 class="main-header">👤 Your Profile</h1>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("""
        <div style="text-align: center;">
            <div style="width: 150px; height: 150px; background: linear-gradient(135deg, #3b82f6, #8b5cf6); 
                    border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 20px auto;">
                <span style="font-size: 4rem;">👤</span>
            </div>
            <h3 style="margin: 0 0 5px 0;">Alex Johnson</h3>
            <p style="color: #94a3b8; margin: 0 0 20px 0;">Premium Member since 2022</p>
            
            <div style="background: #1e293b; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
                <div style="color: #fbbf24; font-size: 2rem; margin-bottom: 5px;">🎯</div>
                <div style="color: white; font-weight: bold;">1,250</div>
                <div style="color: #94a3b8; font-size: 0.9rem;">Reward Points</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Tabs for different sections
        tab1, tab2, tab3 = st.tabs(["📝 Personal Info", "🎟️ Booking History", "⭐ Preferences"])
        
        with tab1:
            with st.form("profile_form"):
                col1, col2 = st.columns(2)
                with col1:
                    first_name = st.text_input("First Name", "Alex")
                    email = st.text_input("Email", "alex.johnson@example.com")
                    phone = st.text_input("Phone", "+1 (555) 123-4567")
                
                with col2:
                    last_name = st.text_input("Last Name", "Johnson")
                    dob = st.date_input("Date of Birth", datetime(1990, 5, 15))
                    country = st.selectbox("Country", ["USA", "Canada", "UK", "Australia"])
                
                if st.form_submit_button("💾 Save Changes", use_container_width=True):
                    st.success("Profile updated successfully!")
        
        with tab2:
            if st.session_state.bookings:
                for booking in st.session_state.bookings[-3:]:  # Show last 3 bookings
                    st.markdown(f"""
                    <div class="movie-card">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <h4 style="margin: 0 0 5px 0;">{booking['movie']['title']}</h4>
                                <p style="color: #94a3b8; margin: 0 0 5px 0;">{booking['theater']} • {booking['showtime']}</p>
                                <p style="color: #94a3b8; margin: 0;">Seats: {', '.join(booking['seats'])}</p>
                            </div>
                            <div style="text-align: right;">
                                <div style="color: #60a5fa; font-weight: bold; font-size: 1.2rem;">${booking['total']}</div>
                                <div style="color: #10b981; font-size: 0.8rem; margin-top: 5px;">{booking['status']}</div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No booking history found.")
        
        with tab3:
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**🎭 Preferred Genres**")
                genres = st.multiselect("Select genres", ["Action", "Comedy", "Drama", "Sci-Fi", "Thriller", "Romance"],
                                      default=["Action", "Sci-Fi"])
                
                st.markdown("**🎦 Theater Preferences**")
                theater_type = st.selectbox("Preferred format", ["IMAX", "4DX", "Dolby Atmos", "Standard"])
            
            with col2:
                st.markdown("**💺 Seat Preferences**")
                seat_pref = st.selectbox("Favorite seats", ["Middle Center", "Back Row", "Front Row", "Aisle"])
                
                st.markdown("**🍿 Snack Preferences**")
                snacks = st.multiselect("Favorite snacks", ["Popcorn", "Nachos", "Candy", "Soft Drink", "Hot Dog"])

# Main App
def main():
    # Initialize page in session state
    if 'page' not in st.session_state:
        st.session_state.page = "🎥 Home"
    
    # Navigation
    page = navigation()
    
    # Page routing
    if page == "🎥 Home":
        home_page()
    elif page == "📽️ Movies":
        movies_page()
    elif page == "🎟️ Book Tickets":
        booking_page()
    elif page == "🎭 Theaters":
        theaters_page()
    elif page == "📊 Analytics":
        analytics_page()
    elif page == "🛒 Cart":
        cart_page()
    elif page == "👤 Profile":
        profile_page()
    
    # Confetti effect (if triggered)
    if st.session_state.show_confetti:
        st.markdown("""
        <div class="confetti-container" id="confetti"></div>
        <script>
            // Simple confetti effect
            const confetti = document.getElementById('confetti');
            for(let i = 0; i < 150; i++) {
                const particle = document.createElement('div');
                particle.style.position = 'absolute';
                particle.style.width = '10px';
                particle.style.height = '10px';
                particle.style.background = `hsl(${Math.random() * 360}, 100%, 60%)`;
                particle.style.borderRadius = '50%';
                particle.style.left = Math.random() * 100 + 'vw';
                particle.style.top = '-10px';
                particle.style.animation = `fall ${Math.random() * 3 + 2}s linear forwards`;
                confetti.appendChild(particle);
                
                // Remove after animation
                setTimeout(() => particle.remove(), 5000);
            }
            
            // Add CSS animation
            const style = document.createElement('style');
            style.textContent = `
                @keyframes fall {
                    to {
                        transform: translateY(100vh) rotate(${Math.random() * 720}deg);
                        opacity: 0;
                    }
                }
            `;
            document.head.appendChild(style);
            
            // Remove confetti after 5 seconds
            setTimeout(() => {
                confetti.remove();
            }, 5000);
        </script>
        """, unsafe_allow_html=True)
        st.session_state.show_confetti = False
    
    # Footer
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**CineMagic Premium**")
        st.markdown("© 2024 All rights reserved")
    with col2:
        st.markdown("**🎬 Experience Excellence**")
        st.markdown("📞 +1 (800) CINE-MAGIC")
        st.markdown("✉️ support@cinemagic.com")
    with col3:
        st.markdown("**Follow Us**")
        st.markdown("🐦 Twitter | 📘 Facebook | 📸 Instagram | 🎬 TikTok")

if __name__ == "__main__":
    main()
