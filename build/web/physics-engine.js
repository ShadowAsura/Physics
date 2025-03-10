// Physics Engine Implementation
import * as THREE from 'https://cdn.jsdelivr.net/npm/three@v0.149.0/build/three.module.js';

// Main physics engine class
class PhysicsEngine {
    constructor(container) {
        this.container = container;
        this.scene = new THREE.Scene();
        this.camera = new THREE.PerspectiveCamera(75, container.clientWidth / container.clientHeight, 0.1, 1000);
        this.renderer = new THREE.WebGLRenderer({ antialias: true });
        this.renderer.setSize(container.clientWidth, container.clientHeight);
        this.container.appendChild(this.renderer.domElement);
        
        // Physics parameters
        this.params = {
            gravity: 9.8,
            elasticity: 0.7,
            friction: 0.3,
            springStiffness: 0.5
        };
        
        // Collections for simulation objects
        this.objects = [];
        this.springs = [];
        
        // Setup camera
        this.camera.position.z = 10;
        
        // Mouse interaction
        this.raycaster = new THREE.Raycaster();
        this.mouse = new THREE.Vector2();
        this.selectedObject = null;
        this.isDragging = false;
        
        // Bind event listeners
        this.setupEventListeners();
        
        // Start animation loop
        this.animate();
    }
    
    setupEventListeners() {
        // Window resize
        window.addEventListener('resize', () => {
            this.renderer.setSize(this.container.clientWidth, this.container.clientHeight);
            this.camera.aspect = this.container.clientWidth / this.container.clientHeight;
            this.camera.updateProjectionMatrix();
        });
        
        // Mouse events for object interaction
        this.container.addEventListener('mousemove', this.onMouseMove.bind(this));
        this.container.addEventListener('mousedown', this.onMouseDown.bind(this));
        this.container.addEventListener('mouseup', this.onMouseUp.bind(this));
        
        // UI controls
        document.getElementById('gravity').addEventListener('input', (e) => {
            this.params.gravity = parseFloat(e.target.value);
            document.getElementById('gravity-value').textContent = this.params.gravity.toFixed(1);
        });
        
        document.getElementById('elasticity').addEventListener('input', (e) => {
            this.params.elasticity = parseFloat(e.target.value);
            document.getElementById('elasticity-value').textContent = this.params.elasticity.toFixed(2);
        });
        
        document.getElementById('friction').addEventListener('input', (e) => {
            this.params.friction = parseFloat(e.target.value);
            document.getElementById('friction-value').textContent = this.params.friction.toFixed(2);
        });
        
        document.getElementById('spring-stiffness').addEventListener('input', (e) => {
            this.params.springStiffness = parseFloat(e.target.value);
            document.getElementById('spring-stiffness-value').textContent = this.params.springStiffness.toFixed(2);
            
            // Update all springs with new stiffness
            this.springs.forEach(spring => {
                spring.stiffness = this.params.springStiffness;
            });
        });
        
        // Add elements buttons
        document.getElementById('add-ball').addEventListener('click', () => this.addBall());
        document.getElementById('add-box').addEventListener('click', () => this.addBox());
        document.getElementById('add-spring').addEventListener('click', () => this.addSpring());
        document.getElementById('add-pendulum').addEventListener('click', () => this.addPendulum());
        
        // Reset button
        document.getElementById('reset-btn').addEventListener('click', () => this.reset());
        
        // Settings button to toggle control UI
        document.getElementById('settings-btn').addEventListener('click', () => {
            const controlUI = document.getElementById('control-ui');
            controlUI.classList.toggle('visible');
        });
    }
    
    onMouseMove(event) {
        // Calculate mouse position in normalized device coordinates
        const rect = this.container.getBoundingClientRect();
        this.mouse.x = ((event.clientX - rect.left) / this.container.clientWidth) * 2 - 1;
        this.mouse.y = -((event.clientY - rect.top) / this.container.clientHeight) * 2 + 1;
        
        // Handle dragging objects
        if (this.isDragging && this.selectedObject) {
            this.raycaster.setFromCamera(this.mouse, this.camera);
            const intersectPlane = new THREE.Plane(new THREE.Vector3(0, 0, 1), 0);
            const targetPosition = new THREE.Vector3();
            this.raycaster.ray.intersectPlane(intersectPlane, targetPosition);
            
            // Update object position
            this.selectedObject.position.copy(targetPosition);
            
            // Reset velocity when dragging
            if (this.selectedObject.userData.physics) {
                this.selectedObject.userData.physics.velocity.set(0, 0, 0);
            }
        }
    }
    
    onMouseDown(event) {
        // Check for object selection
        this.raycaster.setFromCamera(this.mouse, this.camera);
        const intersects = this.raycaster.intersectObjects(this.objects);
        
        if (intersects.length > 0) {
            this.selectedObject = intersects[0].object;
            this.isDragging = true;
            
            // Show notification
            this.showNotification(`Selected ${this.selectedObject.userData.type}`);
        }
    }
    
    onMouseUp() {
        this.isDragging = false;
        this.selectedObject = null;
    }
    
    addBall(x = 0, y = 5, radius = 0.5, mass = 1) {
        // Create ball geometry and material
        const geometry = new THREE.SphereGeometry(radius, 32, 32);
        const material = new THREE.MeshBasicMaterial({ color: 0x4a90e2 });
        const ball = new THREE.Mesh(geometry, material);
        
        // Set position
        ball.position.set(x, y, 0);
        
        // Add physics properties
        ball.userData.physics = {
            type: 'ball',
            mass: mass,
            radius: radius,
            velocity: new THREE.Vector3(0, 0, 0),
            acceleration: new THREE.Vector3(0, 0, 0)
        };
        
        ball.userData.type = 'ball';
        
        // Add to scene and objects array
        this.scene.add(ball);
        this.objects.push(ball);
        
        this.showNotification('Ball added');
        return ball;
    }
    
    addBox(x = 0, y = 5, width = 1, height = 1, mass = 1) {
        // Create box geometry and material
        const geometry = new THREE.BoxGeometry(width, height, 0.2);
        const material = new THREE.MeshBasicMaterial({ color: 0xff9500 });
        const box = new THREE.Mesh(geometry, material);
        
        // Set position
        box.position.set(x, y, 0);
        
        // Add physics properties
        box.userData.physics = {
            type: 'box',
            mass: mass,
            width: width,
            height: height,
            velocity: new THREE.Vector3(0, 0, 0),
            acceleration: new THREE.Vector3(0, 0, 0),
            angularVelocity: 0,
            angularAcceleration: 0
        };
        
        box.userData.type = 'box';
        
        // Add to scene and objects array
        this.scene.add(box);
        this.objects.push(box);
        
        this.showNotification('Box added');
        return box;
    }
    
    addSpring(x1 = -2, y1 = 5, x2 = 2, y2 = 5, restLength = null, stiffness = null) {
        // Create anchor points if not provided
        const anchor1 = this.addBall(x1, y1, 0.3, 1);
        const anchor2 = this.addBall(x2, y2, 0.3, 1);
        
        // Calculate rest length if not provided
        if (restLength === null) {
            const dx = x2 - x1;
            const dy = y2 - y1;
            restLength = Math.sqrt(dx * dx + dy * dy);
        }
        
        // Use global stiffness if not provided
        if (stiffness === null) {
            stiffness = this.params.springStiffness;
        }
        
        // Create spring line
        const points = [];
        points.push(new THREE.Vector3(x1, y1, 0));
        points.push(new THREE.Vector3(x2, y2, 0));
        
        const geometry = new THREE.BufferGeometry().setFromPoints(points);
        const material = new THREE.LineBasicMaterial({ color: 0xffffff });
        const spring = new THREE.Line(geometry, material);
        
        // Add spring properties
        spring.userData = {
            type: 'spring',
            anchor1: anchor1,
            anchor2: anchor2,
            restLength: restLength,
            stiffness: stiffness
        };
        
        // Add to scene and springs array
        this.scene.add(spring);
        this.springs.push(spring);
        
        this.showNotification('Spring added');
        return spring;
    }
    
    addPendulum(x = 0, y = 8, length = 5, bobMass = 2) {
        // Create anchor point
        const anchor = this.addBall(x, y, 0.3, 0);
        anchor.userData.physics.isStatic = true; // Make anchor static
        anchor.material.color.set(0xff0000); // Red color for anchor
        
        // Create bob
        const bob = this.addBall(x, y - length, 0.5, bobMass);
        
        // Create pendulum spring/rope
        const spring = this.addSpring(x, y, x, y - length, length, 0.8);
        
        this.showNotification('Pendulum added');
        return { anchor, bob, spring };
    }
    
    reset() {
        // Remove all objects from scene
        while (this.objects.length > 0) {
            const object = this.objects.pop();
            this.scene.remove(object);
        }
        
        // Remove all springs from scene
        while (this.springs.length > 0) {
            const spring = this.springs.pop();
            this.scene.remove(spring);
        }
        
        this.showNotification('Simulation reset');
    }
    
    showNotification(message) {
        const notification = document.getElementById('notification');
        notification.textContent = message;
        notification.classList.add('show');
        
        // Hide notification after 2 seconds
        setTimeout(() => {
            notification.classList.remove('show');
        }, 2000);
    }
    
    updatePhysics(deltaTime) {
        // Apply gravity and update positions for all objects
        this.objects.forEach(object => {
            const physics = object.userData.physics;
            if (!physics || physics.isStatic) return;
            
            // Apply gravity
            physics.acceleration.y = -this.params.gravity;
            
            // Update velocity
            physics.velocity.x += physics.acceleration.x * deltaTime;
            physics.velocity.y += physics.acceleration.y * deltaTime;
            
            // Apply damping (air resistance)
            physics.velocity.multiplyScalar(1 - (this.params.friction * 0.1));
            
            // Update position
            object.position.x += physics.velocity.x * deltaTime;
            object.position.y += physics.velocity.y * deltaTime;
            
            // Handle angular motion for boxes
            if (physics.type === 'box') {
                object.rotation.z += physics.angularVelocity * deltaTime;
                physics.angularVelocity += physics.angularAcceleration * deltaTime;
                physics.angularVelocity *= (1 - (this.params.friction * 0.1));
            }
            
            // Reset acceleration
            physics.acceleration.set(0, 0, 0);
            if (physics.type === 'box') {
                physics.angularAcceleration = 0;
            }
            
            // Check for collisions with boundaries
            this.handleBoundaryCollisions(object);
        });
        
        // Update springs
        this.springs.forEach(spring => {
            const anchor1 = spring.userData.anchor1;
            const anchor2 = spring.userData.anchor2;
            const restLength = spring.userData.restLength;
            const stiffness = spring.userData.stiffness;
            
            // Calculate current length
            const dx = anchor2.position.x - anchor1.position.x;
            const dy = anchor2.position.y - anchor1.position.y;
            const currentLength = Math.sqrt(dx * dx + dy * dy);
            
            // Calculate spring force (Hooke's Law: F = -k * (x - x0))
            const displacement = currentLength - restLength;
            const forceMagnitude = stiffness * displacement;
            
            // Calculate force direction
            const forceX = (dx / currentLength) * forceMagnitude;
            const forceY = (dy / currentLength) * forceMagnitude;
            
            // Apply forces to anchors (if they're not static)
            if (!anchor1.userData.physics.isStatic) {
                anchor1.userData.physics.acceleration.x += forceX / anchor1.userData.physics.mass;
                anchor1.userData.physics.acceleration.y += forceY / anchor1.userData.physics.mass;
            }
            
            if (!anchor2.userData.physics.isStatic) {
                anchor2.userData.physics.acceleration.x -= forceX / anchor2.userData.physics.mass;
                anchor2.userData.physics.acceleration.y -= forceY / anchor2.userData.physics.mass;
            }
            
            // Update spring line geometry
            const points = [];
            points.push(new THREE.Vector3(anchor1.position.x, anchor1.position.y, 0));
            points.push(new THREE.Vector3(anchor2.position.x, anchor2.position.y, 0));
            
            const geometry = new THREE.BufferGeometry().setFromPoints(points);
            spring.geometry.dispose();
            spring.geometry = geometry;
        });
        
        // Check for collisions between objects
        this.handleObjectCollisions();
    }
    
    handleBoundaryCollisions(object) {
        const physics = object.userData.physics;
        const bounds = {
            left: -9,
            right: 9,
            bottom: -8,
            top: 8
        };
        
        if (physics.type === 'ball') {
            // Ball boundary collision
            const radius = physics.radius;
            
            // Left and right boundaries
            if (object.position.x - radius < bounds.left) {
                object.position.x = bounds.left + radius;
                physics.velocity.x = -physics.velocity.x * this.params.elasticity;
            } else if (object.position.x + radius > bounds.right) {
                object.position.x = bounds.right - radius;
                physics.velocity.x = -physics.velocity.x * this.params.elasticity;
            }
            
            // Bottom and top boundaries
            if (object.position.y - radius < bounds.bottom) {
                object.position.y = bounds.bottom + radius;
                physics.velocity.y = -physics.velocity.y * this.params.elasticity;
                
                // Apply friction when hitting the ground
                physics.velocity.x *= (1 - this.params.friction);
            } else if (object.position.y + radius > bounds.top) {
                object.position.y = bounds.top - radius;
                physics.velocity.y = -physics.velocity.y * this.params.elasticity;
            }
        } else if (physics.type === 'box') {
            // Box boundary collision
            const halfWidth = physics.width / 2;
            const halfHeight = physics.height / 2;
            
            // Left and right boundaries
            if (object.position.x - halfWidth < bounds.left) {
                object.position.x = bounds.left + halfWidth;
                physics.velocity.x = -physics.velocity.x * this.params.elasticity;
            } else if (object.position.x + halfWidth > bounds.right) {
                object.position.x = bounds.right - halfWidth;
                physics.velocity.x = -physics.velocity.x * this.params.elasticity;
            }
            
            // Bottom and top boundaries
            if (object.position.y - halfHeight < bounds.bottom) {
                object.position.y = bounds.bottom + halfHeight;
                physics.velocity.y = -physics.velocity.y * this.params.elasticity;
                
                // Apply friction when hitting the ground
                physics.velocity.x *= (1 - this.params.friction);
                physics.angularVelocity *= (1 - this.params.friction);
            } else if (object.position.y + halfHeight > bounds.top) {
                object.position.y = bounds.top - halfHeight;
                physics.velocity.y = -physics.velocity.y * this.params.elasticity;
            }
        }
    }
    
    handleObjectCollisions() {
        // Check for collisions between all pairs of objects
        for (let i = 0; i < this.objects.length; i++) {
            for (let j = i + 1; j < this.objects.length; j++) {
                const obj1 = this.objects[i];
                const obj2 = this.objects[j];
                
                // Skip if either object is static
                if ((obj1.userData.physics && obj1.userData.physics.isStatic) && 
                    (obj2.userData.physics && obj2.userData.physics.isStatic)) {
                    continue;
                }
                
                // Ball-ball collision
                if (obj1.userData.physics.type === 'ball' && obj2.userData.physics.type === 'ball') {
                    this.handleBallBallCollision(obj1, obj2);
                }
                // Ball-box collision
                else if (obj1.userData.physics.type === 'ball' && obj2.userData.physics.type === 'box') {
                    this.handleBallBoxCollision(obj1, obj2);
                }
                // Box-ball collision
                else if (obj1.userData.physics.type === 'box' && obj2.userData.physics.type === 'ball') {
                    this.handleBallBoxCollision(obj2, obj1);
                }
                // Box-box collision
                else if (obj1.userData.physics.type === 'box' && obj2.userData.physics.type === 'box') {
                    this.handleBoxBoxCollision(obj1, obj2);
                }
            }
        }
    }
    
    handleBallBallCollision(ball1, ball2) {
        const p1 = ball1.position;
        const p2 = ball2.position;
        const r1 = ball1.userData.physics.radius;
        const r2 = ball2.userData.physics.radius;
        
        // Calculate distance between centers
        const dx = p2.x - p1.x;
        const dy = p2.y - p1.y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        
        // Check if balls are colliding
        if (distance < r1 + r2) {
            // Calculate collision normal
            const nx = dx / distance;
            const ny = dy / distance;
            
            // Calculate relative velocity
            const v1 = ball1.userData.physics.velocity;
            const v2 = ball2.userData.physics.velocity;
            const relVelX = v2.x - v1.x;
            const relVelY = v2.y - v1.y;
            
            // Calculate relative velocity along normal
            const relVelDotNormal = relVelX * nx + relVelY * ny;
            
            // If objects are moving away from each other, do nothing
            if (relVelDotNormal > 0) return;
            
            // Calculate impulse scalar
            const m1 = ball1.userData.physics.mass;
            const m2 = ball2.userData.physics.mass;
            const e = this.params.elasticity;
            const j = -(1 + e) * relVelDotNormal / (1/m1 + 1/m2);
            
            // Apply impulse
            const impulseX = j * nx;
            const impulseY = j * ny;
            
            v1.x -= impulseX / m1;
            v1.y -= impulseY / m1;
            v2.x += impulseX / m2;
            v2.y += impulseY / m2;
            
            // Separate balls to prevent sticking
            const overlap = (r1 + r2) - distance;
            const separationX = nx * overlap * 0.5;
            const separationY = ny * overlap * 0.5;
            
            if (!ball1.userData.physics.isStatic) {
                p1.x -= separationX;
                p1.y -= separationY;
            }
            
            if (!ball2.userData.physics.isStatic) {
                p2.x += separationX;
                p2.y += separationY;
            }
        }
    }
    
    handleBallBoxCollision(ball, box) {
        // Simplified ball-box collision
        const ballPos = ball.position;
        const boxPos = box.position;
        const ballRadius = ball.userData.physics.radius;
        const boxHalfWidth = box.userData.physics.width / 2;
        const boxHalfHeight = box.userData.physics.height / 2;
        
        // Find closest point on box to ball center
        const closestX = Math.max(boxPos.x - boxHalfWidth, Math.min(ballPos.x, boxPos.x + boxHalfWidth));
        const closestY = Math.max(boxPos.y - boxHalfHeight, Math.min(ballPos.y, boxPos.y + boxHalfHeight));
        
        // Calculate distance from closest point to ball center
        const dx = closestX - ballPos.x;
        const dy = closestY - ballPos.y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        
        // Check if ball is colliding with box
        if (distance < ballRadius) {
            // Calculate collision normal
            let nx = -dx;
            let ny = -dy;
            
            // If closest point is inside ball, use box face normal
            if (distance === 0) {
                // Determine which face of the box the ball is closest to
                const xDist = Math.min(
                    Math.abs(ballPos.x - (boxPos.x - boxHalfWidth)),
                    Math.abs(ballPos.x - (boxPos.x + boxHalfWidth))
                );
                
                const yDist = Math.min(
                    Math.abs(ballPos.y - (boxPos.y - boxHalfHeight)),
                    Math.abs(ballPos.y - (boxPos.y + boxHalfHeight))
                );
                
                if (xDist < yDist) {
                    nx = ballPos.x < boxPos.x ? -1 : 1;
                    ny = 0;
                } else {
                    nx = 0;
                    ny = ballPos.y < boxPos.y ? -1 : 1;
                }
            } else {
                // Normalize the collision normal
                const len = Math.sqrt(nx * nx + ny * ny);
                nx /= len;
                ny /= len;
            }
            
            // Calculate relative velocity
            const ballVel = ball.userData.physics.velocity;
            const boxVel = box.userData.physics.velocity;
            const relVelX = boxVel.x - ballVel.x;
            const relVelY = boxVel.y - ballVel.y;
            
            // Calculate relative velocity along normal
            const relVelDotNormal = relVelX * nx + relVelY * ny;
            
            // If objects are moving away from each other, do nothing
            if (relVelDotNormal > 0) return;
            
            // Calculate impulse scalar
            const ballMass = ball.userData.physics.mass;
            const boxMass = box.userData.physics.mass;
            const e = this.params.elasticity;
            const j = -(1 + e) * relVelDotNormal / (1/ballMass + 1/boxMass);
            
            // Apply impulse
            const impulseX = j * nx;
            const impulseY = j * ny;
            
            if (!ball.userData.physics.isStatic) {
                ballVel.x -= impulseX / ballMass;
                ballVel.y -= impulseY / ballMass;
            }
            
            if (!box.userData.physics.isStatic) {
                boxVel.x += impulseX / boxMass;
                boxVel.y += impulseY / boxMass;
                
                // Apply torque to box
                const rx = closestX - boxPos.x;
                const ry = closestY - boxPos.y;
                const torque = rx * impulseY - ry * impulseX;
                box.userData.physics.angularAcceleration += torque / (boxMass * (boxHalfWidth * boxHalfWidth + boxHalfHeight * boxHalfHeight) / 6);
            }
            
            // Separate objects to prevent sticking
            const overlap = ballRadius - distance;
            const separationX = nx * overlap;
            const separationY = ny * overlap;
            
            if (!ball.userData.physics.isStatic) {
                ballPos.x -= separationX;
                ballPos.y -= separationY;
            }
            
            if (!box.userData.physics.isStatic) {
                boxPos.x += separationX;
                boxPos.y += separationY;
            }
        }
    }
    
    handleBoxBoxCollision(box1, box2) {
        // Simplified box-box collision using Separating Axis Theorem
        // This is a simplified implementation and could be improved
        const pos1 = box1.position;
        const pos2 = box2.position;
        const w1 = box1.userData.physics.width;
        const h1 = box1.userData.physics.height;
        const w2 = box2.userData.physics.width;
        const h2 = box2.userData.physics.height;
        
        // Check for overlap using AABB (Axis-Aligned Bounding Box)
        const overlapX = Math.min(pos1.x + w1/2, pos2.x + w2/2) - Math.max(pos1.x - w1/2, pos2.x - w2/2);
        const overlapY = Math.min(pos1.y + h1/2, pos2.y + h2/2) - Math.max(pos1.y - h1/2, pos2.y - h2/2);
        
        if (overlapX > 0 && overlapY > 0) {
            // Determine collision normal based on smallest overlap
            let nx = 0;
            let ny = 0;
            
            if (overlapX < overlapY) {
                nx = pos1.x < pos2.x ? -1 : 1;
            } else {
                ny = pos1.y < pos2.y ? -1 : 1;
            }
            
            // Calculate relative velocity
            const v1 = box1.userData.physics.velocity;
            const v2 = box2.userData.physics.velocity;
            const relVelX = v2.x - v1.x;
            const relVelY = v2.y - v1.y;
            
            // Calculate relative velocity along normal
            const relVelDotNormal = relVelX * nx + relVelY * ny;
            
            // If objects are moving away from each other, do nothing
            if (relVelDotNormal > 0) return;
            
            // Calculate impulse scalar
            const m1 = box1.userData.physics.mass;
            const m2 = box2.userData.physics.mass;
            const e = this.params.elasticity;
            const j = -(1 + e) * relVelDotNormal / (1/m1 + 1/m2);
            
            // Apply impulse
            const impulseX = j * nx;
            const impulseY = j * ny;
            
            if (!box1.userData.physics.isStatic) {
                v1.x -= impulseX / m1;
                v1.y -= impulseY / m1;
            }
            
            if (!box2.userData.physics.isStatic) {
                v2.x += impulseX / m2;
                v2.y += impulseY / m2;
            }
            
            // Separate boxes to prevent sticking
            const overlap = (overlapX < overlapY) ? overlapX : overlapY;
            const separationX = nx * overlap * 0.5;
            const separationY = ny * overlap * 0.5;
            
            if (!box1.userData.physics.isStatic) {
                pos1.x -= separationX;
                pos1.y -= separationY;
            }
            
            if (!box2.userData.physics.isStatic) {
                pos2.x += separationX;
                pos2.y += separationY;
            }
        }
    }
    
    animate() {
        requestAnimationFrame(this.animate.bind(this));
        
        // Calculate delta time (capped to prevent large jumps)
        const now = performance.now();
        const deltaTime = Math.min((now - (this.lastTime || now)) / 1000, 0.05);
        this.lastTime = now;
        
        // Update physics
        this.updatePhysics(deltaTime);
        
        // Render scene
        this.renderer.render(this.scene, this.camera);
    }
}

// Initialize the physics engine when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('physics-sim');
    const engine = new PhysicsEngine(container);
    
    // Add some initial objects
    engine.addBall(-3, 5);
    engine.addBox(3, 5);
    engine.addPendulum(0, 8);
    
    // Show initial notification
    engine.showNotification('Physics engine initialized');
});