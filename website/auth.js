// auth.js
import { initializeApp } from "https://www.gstatic.com/firebasejs/11.3.1/firebase-app.js";
import { 
    getAuth, 
    createUserWithEmailAndPassword,
    signInWithEmailAndPassword,
    GoogleAuthProvider,
    signInWithPopup,
    onAuthStateChanged,
    signOut 
} from "https://www.gstatic.com/firebasejs/11.3.1/firebase-auth.js";

const firebaseConfig = {
    apiKey: "AIzaSyDIpfaXN09X61hsMX2H_g6rZrJxdCmLMH0",
    authDomain: "devops-supermarket.firebaseapp.com",
    projectId: "devops-supermarket",
    storageBucket: "devops-supermarket.firebasestorage.app",
    messagingSenderId: "519026284858",
    appId: "1:519026284858:web:2a3ae902a82cc6d3a05803",
    measurementId: "G-T13TKWLJ53"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

// Modal elements
const modal = document.getElementById('authModal');
const loginButton = document.querySelector('.user-controls');
const closeModal = document.querySelector('.close-modal');

// Show modal when clicking login button
loginButton.addEventListener('click', () => {
    modal.classList.add('show');
});

// Close modal when clicking X or outside
closeModal.addEventListener('click', () => {
    modal.classList.remove('show');
});

window.addEventListener('click', (e) => {
    if (e.target === modal) {
        modal.classList.remove('show');
    }
});

// Tab switching
const tabButtons = document.querySelectorAll('.tab-btn');
const authForms = document.querySelectorAll('.auth-form');

tabButtons.forEach(button => {
    button.addEventListener('click', () => {
        const tabName = button.getAttribute('data-tab');
        tabButtons.forEach(btn => btn.classList.remove('active'));
        button.classList.add('active');
        
        authForms.forEach(form => {
            form.classList.remove('active');
            if (form.id === `${tabName}Form`) {
                form.classList.add('active');
            }
        });
    });
});

// Login form
const loginForm = document.getElementById('loginForm');
loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;
    
    try {
        await signInWithEmailAndPassword(auth, email, password);
        modal.classList.remove('show');
        updateUIForUser();
    } catch (error) {
        showError(loginForm, error.message);
    }
});

// Register form
const registerForm = document.getElementById('registerForm');
registerForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const email = document.getElementById('registerEmail').value;
    const password = document.getElementById('registerPassword').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    const name = document.getElementById('registerName').value;
    
    if (password !== confirmPassword) {
        showError(registerForm, "Passwords don't match");
        return;
    }
    
    try {
        const userCredential = await createUserWithEmailAndPassword(auth, email, password);
        modal.classList.remove('show');
        updateUIForUser();
    } catch (error) {
        showError(registerForm, error.message);
    }
});

// Google Sign-in
const googleButton = document.querySelector('.google-button');
googleButton.addEventListener('click', async () => {
    const provider = new GoogleAuthProvider();
    try {
        await signInWithPopup(auth, provider);
        modal.classList.remove('show');
        updateUIForUser();
    } catch (error) {
        showError(loginForm, error.message);
    }
});

// Update UI based on auth state
function updateUIForUser() {
    const user = auth.currentUser;
    const userControls = document.querySelector('.user-controls');
    
    if (user) {
        userControls.innerHTML = `
            <i class="fas fa-user"></i>
            <span>${user.displayName || user.email}</span>
            <button class="logout-button">Logout</button>
            <i class="fas fa-question-circle"></i>
            <span>Help Centre</span>
        `;
        
        // Add logout functionality
        const logoutButton = document.querySelector('.logout-button');
        logoutButton.addEventListener('click', async () => {
            try {
                await signOut(auth);
            } catch (error) {
                console.error('Error signing out:', error);
            }
        });
    } else {
        userControls.innerHTML = `
            <i class="fas fa-user"></i>
            <span>Login/Sign up</span>
            <i class="fas fa-question-circle"></i>
            <span>Help Centre</span>
        `;
    }
}

// Show error message
function showError(form, message) {
    const existingError = form.querySelector('.error-message');
    if (existingError) {
        existingError.remove();
    }
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    form.appendChild(errorDiv);
}

// Initialize UI based on auth state
onAuthStateChanged(auth, (user) => {
    updateUIForUser();
});