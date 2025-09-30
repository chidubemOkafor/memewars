"use client";

import { useRouter } from "next/navigation";
import React, { use, useEffect } from 'react'
import axios from 'axios'

const SignIn = () => {
    const [authUrl, setAuthUrl] = React.useState('')
    const router = useRouter()
    useEffect(() => {
        const url = async() => {
            const url = await axios.get('http://localhost:8000/auth')
            setAuthUrl(url.data.url)
            return url.data.url
        }
        url()
    } , [])

    const handleRedirect = () => {
        router.push(authUrl);
    };

  return (
    <div>
        <button
        onClick={handleRedirect}
      className="px-4 py-2 bg-blue-500 text-white rounded-lg shadow hover:bg-blue-600 transition"
    >
      Login with Twitters
    </button>
  

    </div>
  )
}

export default SignIn
