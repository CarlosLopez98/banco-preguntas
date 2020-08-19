/* ROLES */
INSERT INTO roles VALUES(null, 'admin');
INSERT INTO roles VALUES(null, 'docente');
INSERT INTO roles VALUES(null, 'estudiante');

/* USUARIOS */
INSERT INTO usuarios VALUES(null, 'admin', 'admin', 'admin@mail.com', 'pbkdf2:sha256:150000$ZELxW1JV$e2f830d66c253d8430a13c1be37371254e93eca040d9476d8f40c70495df7a0d', 1);
INSERT INTO usuarios VALUES(null, 'profe', 'profe', 'profe@mail.com', 'pbkdf2:sha256:150000$A1phZe6D$b46205ca17fd975f02f87e401474f59e3eae1668980c38acd621f4a61e23a98d', 2);
INSERT INTO usuarios VALUES(null, 'estudiante', 'estudiante', 'estudiante@mail.com', 'pbkdf2:sha256:150000$UpMUkQ4t$47d12be0e858ffd2e70171266ed869861ea38e4cf55a6f1c632b53defcc47170', 3);

/*  */