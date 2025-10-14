import { useState, useEffect } from 'react';
import LoginModal from './LoginModal';
import SignupModal from './SignupModal';
import './Header.css';

function Header({ onSearchChange }) {
  const [showLoginModal, setShowLoginModal] = useState(false);
  const [showSignupModal, setShowSignupModal] = useState(false);
  const [isScrolled, setIsScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 50);
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const scrollToSection = (id) => {
    const element = document.getElementById(id);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <>
      <header className={`netflix-header ${isScrolled ? 'scrolled' : ''}`}>
        <div className="header-container">
          <div className="header-left">
            <h1 className="app-logo">Anuvaad AI</h1>
            <nav className="nav-links">
              <a onClick={() => scrollToSection('hero')}>Home</a>
              <a onClick={() => scrollToSection('features')}>Features</a>
              <a onClick={() => scrollToSection('tools')}>Tools</a>
              <a onClick={() => scrollToSection('footer')}>Contact</a>
            </nav>
          </div>
          
          <div className="header-right">
            <button className="btn-login" onClick={() => setShowLoginModal(true)}>
              Log In
            </button>
            <button className="btn-signup" onClick={() => setShowSignupModal(true)}>
              Sign Up
            </button>
          </div>
        </div>
      </header>

      {showLoginModal && <LoginModal onClose={() => setShowLoginModal(false)} />}
      {showSignupModal && <SignupModal onClose={() => setShowSignupModal(false)} />}
    </>
  );
}

export default Header;
