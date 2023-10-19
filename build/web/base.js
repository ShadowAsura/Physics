// Setting up the scene, camera, and renderer
// Setting up the scene, camera, and renderer
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer();

let container = document.getElementById('fluid-sim');
renderer.setSize(container.clientWidth, container.clientHeight);
container.appendChild(renderer.domElement);

// Particle properties
const particleCount = 500;
let particles = [];
let selectedParticles = [];
maxVelocity = 3.0

let isMousePressed = false;
let capturedParticles = [];


const params = {
    gravity: 0.005,
    cohesionDistance: 0.2,
    separationDistance: 0.1,
    cohesionScalar: 0.01,
    separationScalar: 0.02,
    damping: 0.96,
    bounceDamping: -0.5
};

window.addEventListener('resize', function () {
    // Update sizes based on the container
    renderer.setSize(container.clientWidth, container.clientHeight);
    camera.aspect = container.clientWidth / container.clientHeight;
    camera.updateProjectionMatrix();
});


// Adjust mouse event listeners to listen to container instead of the whole window
container.addEventListener('mousemove', onMouseMove, false);
container.addEventListener('mousedown', onMouseClick, false);


const mousePos = new THREE.Vector2();

window.addEventListener('mousemove', (event) => {
    mousePos.x = (event.clientX / window.innerWidth) * 2 - 1;
    mousePos.y = -(event.clientY / window.innerHeight) * 2 + 1;
});

window.addEventListener('mousedown', () => {
    isMousePressed = true;
    capturedParticles = [];
    particles.forEach(particle => {
        const dx = particle.position.x - mousePos.x * 5;
        const dy = particle.position.y - mousePos.y * 5;
        const distance = Math.sqrt(dx * dx + dy * dy);
        if (distance < 0.5) {
            capturedParticles.push(particle);
        }
    });
}, { passive: true });

window.addEventListener('mouseup', () => {
    isMousePressed = false;
    capturedParticles = [];
}, { passive: true });

function applyMouseDrag() {
    if (isMousePressed) {
        capturedParticles.forEach(particle => {
            particle.position.x += (mousePos.x * 5 - particle.position.x) * 0.1;
            particle.position.y += (mousePos.y * 5 - particle.position.y) * 0.1;
        });
    }
}




function createParticles() {
    const geometry = new THREE.SphereGeometry(0.05);
    for (let i = 0; i < particleCount; i++) {
        const material = new THREE.MeshBasicMaterial({ color: new THREE.Color('blue') });
        const particle = new THREE.Mesh(geometry, material);
        
        particle.position.set(Math.random() * 5 - 2.5, Math.random() * 5 - 2.5, 0);
        particle.velocity = new THREE.Vector3(Math.random() * 2 - 1, Math.random() * 2 - 1, 0);
        
        particles.push(particle);
        scene.add(particle);
    }
}

// Mouse interaction
const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();
function onMouseMove(event) {
    mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
    mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;
}
window.addEventListener('mousemove', onMouseMove, false);

function onMouseClick(event) {
    raycaster.setFromCamera(mouse, camera);
    const intersects = raycaster.intersectObjects(particles);

    for (let i = 0; i < intersects.length; i++) {
        intersects[i].object.material.color.set(0xff0000); // Change color to red
        selectedParticles.push(intersects[i].object);
    }
}
window.addEventListener('mousedown', onMouseClick, false);

function updateParticles() {
    particles.forEach(particle => {
        particle.velocity.multiplyScalar(params.damping);
        particle.velocity.y -= params.gravity;
        particle.position.add(particle.velocity);
        // Velocity to color mapping
        const velocityMagnitude = particle.velocity.length();
        const colorValue = velocityMagnitude / maxVelocity;
        particle.material.color.set(new THREE.Color(getColorFromVelocity(colorValue,5)));
        // Bounce off "walls" (left and right sides)
        if (particle.position.x > 2.5 || particle.position.x < -2.5) {
            particle.velocity.x *= params.bounceDamping;
            if (particle.position.x > 2.5) particle.position.x = 2.5;
            if (particle.position.x < -2.5) particle.position.x = -2.5;
        }
    });
}
function getColorFromVelocity(velocity, velocityFactor = 1) {
    // Define the colors for the highest and lowest velocities
    const colors = [
        {pos: 0, color: new THREE.Color(0x0000FF)}, // Blue
        {pos: 0.25, color: new THREE.Color(0x00FF00)}, // Green
        {pos: 0.5, color: new THREE.Color(0xFFFF00)}, // Yellow
        {pos: 0.75, color: new THREE.Color(0xFFA500)}, // Orange
        {pos: 1, color: new THREE.Color(0xFF0000)} // Red
    ];

    // Scale the velocity by the provided factor
    velocity *= velocityFactor;

    // Find the two colors we need to interpolate between
    let color1, color2;
    for (let i = 0; i < colors.length - 1; i++) {
        if (velocity >= colors[i].pos && velocity <= colors[i + 1].pos) {
            color1 = colors[i];
            color2 = colors[i + 1];
            break;
        }
    }

    // If velocity is out of bounds, clamp it
    if (!color1) {
        return velocity <= 0 ? colors[0].color : colors[colors.length - 1].color;
    }

    // Interpolate between the two colors
    const t = (velocity - color1.pos) / (color2.pos - color1.pos);
    const r = color1.color.r + t * (color2.color.r - color1.color.r);
    const g = color1.color.g + t * (color2.color.g - color1.color.g);
    const b = color1.color.b + t * (color2.color.b - color1.color.b);

    return new THREE.Color(r, g, b);
}


function applyExternalForces() {
    particles.forEach(particle => {
        particle.velocity.y -= 0.01; // Gravity
    });
}
function applyParticleInteractions() {
    particles.forEach(p1 => {
        particles.forEach(p2 => {
            if (p1 !== p2) {
                const dx = p1.position.x - p2.position.x;
                const dy = p1.position.y - p2.position.y;
                const distance = Math.sqrt(dx * dx + dy * dy);

                if (distance < 0.1) {
                    const forceMagnitude = 0.005 / (distance * distance); 
                    const ax = dx * forceMagnitude;
                    const ay = dy * forceMagnitude;

                    p1.velocity.x += ax;
                    p1.velocity.y += ay;
                    p2.velocity.x -= ax;
                    p2.velocity.y -= ay;
                }
            }
        });
    });
}


function applyCohesionAndSeparation() {
    particles.forEach(p1 => {
        let cohesionForce = new THREE.Vector3();
        let separationForce = new THREE.Vector3();

        particles.forEach(p2 => {
            if (p1 !== p2) {
                const distance = p1.position.distanceTo(p2.position);

                if (distance < params.cohesionDistance) {
                    cohesionForce.add(p2.position);
                }

                if (distance < params.separationDistance) {
                    const repelForce = p1.position.clone().sub(p2.position).normalize().multiplyScalar(params.separationScalar);
                    separationForce.add(repelForce);
                }
            }
        });

        cohesionForce.divideScalar(particles.length).sub(p1.position).multiplyScalar(params.cohesionScalar);
        
        p1.velocity.add(cohesionForce);
        p1.velocity.add(separationForce);
        
        if (separationForce.length() > 0.1) {
            p1.velocity.multiplyScalar(0.95);
        }

        // Vertical constraint to make particles settle more naturally
        if (p1.position.y < -2.3 && p1.velocity.y < 0) {
            p1.velocity.y *= -0.2;
        }
    });
}

function animate() {
    requestAnimationFrame(animate);

    applyCohesionAndSeparation();
    applyMouseDrag();
    updateParticles();

    renderer.render(scene, camera);
}
let isSPHMode = false;
// Initialization
function init() {
    camera.position.z = 5;
    createParticles();
    animate();
    const gui = new dat.GUI({ autoPlace: false });
    let container = document.getElementById('fluid-sim');
    container.appendChild(gui.domElement);


    gui.add(params, 'gravity', 0, 0.02);
    gui.add(params, 'cohesionDistance', 0, 1);
    gui.add(params, 'separationDistance', 0, 1);
    gui.add(params, 'cohesionScalar', 0, 0.1);
    gui.add(params, 'separationScalar', 0, 0.1);
    gui.add(params, 'damping', 0.5, 1);
    gui.add(params, 'bounceDamping', -1, 0);
    gui.add({ toggleSPHMode: function() {
        isSPHMode = !isSPHMode;
        const notification = document.getElementById('notification');
        if (isSPHMode) {
            params.gravity = 0.0065;  // Near zero gravity
            params.cohesionDistance = 0.2;  // Set cohesion range
            params.separationDistance = 0.1;  // Set separation range
            params.cohesionScalar = 0;  // No cohesion strength
            params.separationScalar = 0.024;  // Updated separation strength
            params.damping = 0.5;  // Set damping for more viscous feel
            params.bounceDamping = -0.5;  // No bounce damping

            notification.innerText = "SPH Mode activated!";
        } else {
            // Reset to default or other desired parameters
            params.gravity = 0.005;
            params.cohesionDistance = 0.2;
            params.separationDistance = 0.1;
            params.cohesionScalar = 0.01;
            params.separationScalar = 0.02;
            params.damping = 0.96;
            params.bounceDamping = -0.5;

            notification.innerText = "SPH Mode deactivated!";
        }

        notification.classList.add('slide-in'); // Make the notification slide in immediately

        setTimeout(() => {
            notification.classList.add('slide-out');
        }, 2500); // Start easing out after 2.5 seconds

        setTimeout(() => {
            notification.classList.remove('slide-in');
            notification.classList.remove('slide-out');
        }, 3000); // Reset after 3 seconds
    }}, 'toggleSPHMode');

}


// Execute Initialization
init();
