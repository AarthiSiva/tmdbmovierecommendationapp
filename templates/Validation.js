
function validateName() {
	 
	var name = document.myForm.uname;
  	var letters = /^[A-Za-z0-9]+$/;
	if(name.value.match(letters))
	{
		 document.getElementById("name").innerHTML="";
   	return true;
	}
	 else
	{
   	 document.getElementById("name").innerHTML="Username cannot be empty and must contain only numbers and alphabets";  
     document.myForm.uname.focus() ;
      return false;
	}  
    }
function validatePassword() {

var name = document.myForm.pwd;
var letters = /^[A-Za-z0-9@#$]+$/;
if(name.value.match(letters))
{
	document.getElementById("pass").innerHTML="";
	return true;
}
 else
{
document.getElementById("pass").innerHTML="Password cannot be empty and must contain only numbers,alphabets and only these special characters @,#,$";  
document.myForm.uname.focus() ;
  return false;
} 
}
function validateEmail() {
	var mail= myForm.mail.value;
	
	if (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(mail))
	  {
		 document.getElementById("email").innerHTML="";
			return true;
	 
	  }
	else{  
	 document.getElementById("email").innerHTML="Entered Email ID is not valid ";  
	 document.myForm.mail.focus() ;
	  return false;
	}
}
function check() {
	  if (document.getElementById("pwd1").value == document.getElementById("pwd2").value) {
		  
			    document.getElementById("confirmpass").style.color = 'white';
			    document.getElementById("confirmpass").innerHTML = 'Passwords match';
			    document.getElementById("pass").innerHTML="";
			  } else {
			    document.getElementById("confirmpass").style.color = 'red';
			    document.getElementById("confirmpass").innerHTML = 'Passwords do not match'
	            }
	  
	}