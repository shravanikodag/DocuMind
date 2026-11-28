import { useState } from "react";
import "./Auth.css";

function Auth({ onLogin })
{
    const [mode, setMode] = useState("login");
    const [username, setUsername] = useState("");
    const [password,setPassword] = useState("");
    const [confirm, setConfirm] = useState("");
    const [message, setMessage]=useState("");
    const [loading,setLoading]=useState(false);

    const isRegister = mode === "register";

    const handleSubmit = async (event)=>
    {
        event.preventDefault();       //It prevents the browser's default form submission behaviour.
        setLoading(true);
        setMessage("");
        try
        {
            await fetch("/api/auth/csrf/",
            {
                credentials:"same-origin",  
            });
            const token = document.cookie //allow to read cookies are accessible to js on current wp
            .split("; ")
            .find((item) => item.startsWith("csrftoken="))
            ?.split("=")[1] || "";

            const formData = new FormData();
            formData.append("username",username);
            if(isRegister)
            {
                formData.append("password1",password);
                formData.append("password2",confirm);
            }
            else
            {
                    formData.append("password",password);
            }
            
            const url = isRegister ? "/api/auth/register/" : "/api/auth/login/";
            const response = await fetch(url ,{
                    method:"POST",
                    credentials: "same-origin",
                    headers: {"X-CSRFToken":token }, //authentication purpose
                    body:formData,
                });
                
            const data=await response.json(); //to fetch data from backend side

            if (!response.ok) 
            {  //checks whether the HTTP req was successful if true HTTP status code is 200 to 299 else outside of range
                //false asle trr this line will execute
                const errors = data.errors
                ? Object.values(data.errors).flat().join(" ") //flat convets nested array into single level array and join convert into one string with space btween them
                : data.error;
                throw new Error(errors || "Something went wrong.");
            }
            if (isRegister)
            {
                setMode("login");
                setPassword("");
                setConfirm("");
                setMessage("Account created! Please login.");
            } 
            else
            {
                onLogin(data.user);
            }
        }

        catch (error){setMessage(error.message);}
        finally{setLoading(false);}
        
             
    };
}


            
