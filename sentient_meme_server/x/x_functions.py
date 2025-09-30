def get_x_user_details(access_token: str):
    try:
        import requests
        url = "https://api.twitter.com/2/users/me"
        headers = { "Authorization": f"Bearer {access_token}" }
        params = {
            "user.fields": "profile_image_url,verified,description,created_at"
        }
        response = requests.get(url, headers=headers, params=params)
        
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching user details: {e}")
        return None