// Initialize firestore DB
const db = firebase.firestore()

function buyerSignIn(email, password){
    auth.setPersistence(firebase.auth.Auth.Persistence.NONE);
    
    auth.signInWithEmailAndPassword(email, password).then(cred => {
        const userRef = db.collection('User').doc(cred.user.uid);
        userRef.get().then((snapShot)=>{
            userData = snapShot.data();
            if(snapShot.exists && userData.isBuyer){
                alert("Buyer logged in");
                auth.currentUser.getIdToken().then(idToken =>{
                    // csrf Token to be configured later 
                    const csrfToken = getCookie('csrfToken')
                    alert(idToken)
                    // postIdTokenToSessionLogin('/session-login', idToken, csrfToken);
                    data = JSON.stringify({'idToken': idToken, 'csrfToken': csrfToken})
                    var http = new XMLHttpRequest();
                    http.open('POST', '/session-login', false);
                    http.setRequestHeader('Content-type','application/json');
                    http.onreadystatechange = function(){
                        if(this.readyState == 4 && this.status ==200){
                            // alert(this.responseText)
                        }
                    }
                    http.send(data);
                }).then(()=>{
                    window.location="/console/buyer"
                })
            } else{
                alert('wrong credentials');
                signOut();
            }
        })
    }).catch(error =>{
        alert(error)
    })

}

function providerSignIn(email, password){
    auth.setPersistence(firebase.auth.Auth.Persistence.NONE);

    auth.signInWithEmailAndPassword(email, password).then(cred => {
        const userRef = db.collection('User').doc(cred.user.uid);
        userRef.get().then((snapShot)=>{
            userData = snapShot.data();
            if(snapShot.exists && userData.isProvider){
                alert("Provider logged in");
                auth.currentUser.getIdToken().then(idToken =>{
                    // csrf Token to be configured later 
                    const csrfToken = getCookie('csrfToken')
                    alert(idToken)
                    // postIdTokenToSessionLogin('/session-login', idToken, csrfToken);
                    var data = JSON.stringify({'idToken': idToken, 'csrfToken': csrfToken})
                    var http = new XMLHttpRequest();
                    http.open('POST', '/session-login', false);
                    http.setRequestHeader('Content-type','application/json');
                    http.onreadystatechange = function(){
                        if(this.readyState == 4 && this.status ==200){
                            // alert(this.responseText)
                        }
                    }
                    http.send(data);
                    
                }).then(()=>{
                    window.location= "/console/provider"
                })
                
            } else{
                alert('wrong credentials');
                signOut();
            }
        })
    }).catch(error =>{
        alert(error)
    })

}

function getCookie(name) {
    var v = document.cookie.match('(^|;) ?' + name + '=([^;]*)(;|$)');
    return v ? v[2] : null;
}

// ------------------------------------------------
// buyerFlag : true -> buyer
// buyerFlag : false -> provider
// ------------------------------------------------
function signUp(email, password, buyerFlag){  
    alert(email)
    
    var data = JSON.stringify({'email': email, 'buyerFlag':buyerFlag})
    var http = new XMLHttpRequest();

    http.open('POST', "/pre-register", true);
    http.setRequestHeader('Content-type','application/json');
    http.onreadystatechange = function(){
        if(http.readyState == 4){
            if (http.status == 201){
                // User does not exist
                alert(http.responseText)
                auth.createUserWithEmailAndPassword(email, password)
                .then((d) => {
                    var innerHttp = new XMLHttpRequest();
                    var innerData = JSON.stringify({'email': email, 'buyerFlag':buyerFlag, 'id':d.user.uid})
                    innerHttp.open('POST', "/user", true);
                    innerHttp.setRequestHeader('Content-type','application/json');
                    innerHttp.onreadystatechange = function(){
                        if(innerHttp.readyState == 4 && innerHttp.status == 201){
                            alert(innerHttp.responseText);
                            window.location = "/";
                        }
                    }
                    innerHttp.send(innerData)
                }).catch( error =>{
                    alert(error);
                })
            } else if(http.status == 211){
                // User type has been updated
                alert(http.responseText)
                window.location = "/";
            } else if(http.status == 400){
                // User already exists
                alert(http.responseText)
                window.location="/"
                
            }

        } 
    };
    http.send(data);

}