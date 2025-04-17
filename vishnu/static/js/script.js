const title = document.querySelector('.title');
const stock1 = document.querySelector('.stock1');
const stock2 = document.querySelector('.stock2');
const chart1 = document.querySelector('.chart1');
const chart2 = document.querySelector('.chart2');
const graph1 = document.querySelector('.graph1');
const graph2 = document.querySelector('.graph2');

document.addEventListener('scroll', function() {
    let value = window.scrollY;

    // Title movement (you can adjust the parallax intensity for each element here)
    title.style.marginTop = value * 1.1 + 'px';

    // Parallax for stocks and charts (make them move based on scroll position)
    stock1.style.transform = `translateX(${-value * 0.4}px) translateY(${value * 0.2}px)`;
    stock2.style.transform = `translateX(${-value * 0.3}px) translateY(${value * 0.3}px)`;

    chart1.style.transform = `translateX(${value * 0.5}px) translateY(${value * 0.1}px)`;
    chart2.style.transform = `translateX(${value * 0.4}px) translateY(${value * 0.5}px)`;

    graph1.style.transform = `translateX(${value * 0.3}px) translateY(${value * 0.2}px)`;
    graph2.style.transform = `translateX(${-value * 0.2}px) translateY(${value * 0.4}px)`;
});



    // Function to check visibility of elements in viewport
    const fadeInElements = document.querySelectorAll('.fade-in');
    
    const checkVisibility = () => {
        fadeInElements.forEach(element => {
            const rect = element.getBoundingClientRect();
            if (rect.top >= 0 && rect.bottom <= window.innerHeight) {
                element.classList.add('visible');
            } else {
                element.classList.remove('visible');
            }
        });
    };

    // Listen for scroll events
    window.addEventListener('scroll', checkVisibility);

    // Initial check when the page loads
    window.addEventListener('load', checkVisibility);
