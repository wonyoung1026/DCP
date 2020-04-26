// Initiate firebase auth.
function initFirebaseAuth(loggedInCallbackFunc, loggedOutCallbackFunc) {
    auth.onAuthStateChanged(user =>{
        if(user){
            // console.log("USER logged in");
            // loggedInCallbackFunc();
            
		} else{
            // loggedOutCallbackFunc();
            // alert("User not logged in")
            // window.location = "/"
		}
        
	});
}

function getRequestWithIdToken(url){
    auth.currentUser.getIdToken(true).then(function(idToken) {
        // Send token to your backend via HTTPS
        http = new XMLHttpRequest();
        http.open('GET', url, true);
        http.setRequestHeader('Authorization', 'Bearer '+idToken);
        http.send();
        console.log("Call back success");
      }).catch(function(error) {
        // Handle error
        alert(error);
        
      });
}
// Sign Out function
function signOut(){
    auth.signOut().then(() => {
        http = new XMLHttpRequest();
        http.open('POST', '/session-logout', true);
        http.send();
    }).then(()=>{
        alert("Sign out successful");
        window.location = "/"
    }).catch(error =>{
        alert(error)
    });
    
}


// Your web app's Firebase configuration
const firebaseConfig = {
    apiKey: "AIzaSyCk4aPdqLDzquNBl6jiEbuwK8WN2TypCs8",
    authDomain: "decentralized-cloud-platform.firebaseapp.com",
    databaseURL: "https://decentralized-cloud-platform.firebaseio.com",
    projectId: "decentralized-cloud-platform",
};


// Initialize Firebase
firebase.initializeApp(firebaseConfig);
const auth = firebase.auth();
