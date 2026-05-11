export function registerAuthRoutes(app: { post: Function }) {
  app.post("/login", async (request: { body: { email: string; password: string } }) => {
    const email = request.body.email.trim().toLowerCase();
    const password = request.body.password;

    return { email, passwordAccepted: password.length > 0 };
  });
}
