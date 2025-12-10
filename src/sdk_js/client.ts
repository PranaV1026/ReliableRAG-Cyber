import axios from "axios";
import { AskResponse } from "./types.js";

export class ReliableRAG {
  baseUrl: string;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl.replace(/\/$/, "");
  }

  async ask(question: string, context: Record<string, any> = {}): Promise<AskResponse> {
    try {
      const response = await axios.post(`${this.baseUrl}/ask`, {
        question,
        context,
      });

      return response.data as AskResponse;
    } catch (err: any) {
      throw new Error(
        `Request to ReliableRAG failed: ${err?.response?.status} ${err?.response?.data}`
      );
    }
  }
}
