export type SessionResult = {
  userId: string;
  token: string;
  auditEvent: string;
};

export function createSession(userId: string): SessionResult {
  const token = `token-${userId}`;

  return {
    userId,
    token,
    auditEvent: `session.created:${userId}`,
  };
}
