
AOS.init();

const learnMoreButton = document.querySelector('.learn-more');
const nextSection = document.querySelector('#feed-info');

learnMoreButton.addEventListener('click', () => {
    nextSection.scrollIntoView({ behavior: 'smooth' });
});

