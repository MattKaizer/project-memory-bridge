export type DomainEvent = {
  type: string;
  userId: string;
  payload: Record<string, string | boolean>;
};

export function publishDomainEvent(event: DomainEvent) {
  return `${event.type}:${event.userId}`;
}
