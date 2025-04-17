// Navbar Transparency on Scroll
window.addEventListener('scroll', () => {
    const navbar = document.getElementById('navbar');
    if (window.scrollY > 100) {
      navbar.classList.remove('transparent');
    } else {
      navbar.classList.add('transparent');
    }
  });
  
  // Fade-in Animations on Scroll
  const fadeIns = document.querySelectorAll('.step, .value-point, .value-image');
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('fade-in');
      }
    });
  }, { threshold: 0.5 });
  
  fadeIns.forEach(fadeIn => observer.observe(fadeIn));
  
  // Project Counter Animation
  const projectCount = document.getElementById('project-count');
  let count = 0;
  const targetCount = 203; // Replace with your actual project count
  const interval = setInterval(() => {
    if (count >= targetCount) {
      clearInterval(interval);
    } else {
      count++;
      projectCount.textContent = count;
    }
  }, 10);