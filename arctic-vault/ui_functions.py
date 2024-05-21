import base64
from pathlib import Path

def render_app_logo() -> str:
    
    logo = f"url(data:image/png;base64,{base64.b64encode(Path('static/arctic-vault.png').read_bytes()).decode()})"

    logo_str = f"""
        <style>
            [data-testid="stSidebarNav"] {{
                background-image: {logo};
                background-repeat: no-repeat;
                background-position: 20px 50px;
                background-size: 200px 200px;
                padding-top: 200px
            }}
        </style>
    """

    return logo_str