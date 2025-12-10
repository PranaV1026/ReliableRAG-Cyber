export interface AskResponse {
  answer: string;
  confidence: number;
  risk: string;
  reasons: string[];
  sources: string[];
}
