// config.js – Fill in your credentials here
export const SUPABASE_URL = "YOUR_SUPABASE_URL"; // e.g., https://xxxxx.supabase.co
export const SUPABASE_ANON_KEY = "YOUR_SUPABASE_ANON_KEY";
export const GEMINI_API_KEY = "YOUR_GEMINI_API_KEY";

// Optional: Export a fetch wrapper for Gemini
export async function classifyDifficulty(taskText) {
  const prompt = `Classify the difficulty of this task as Easy, Medium, or Hard.\nTask: "${taskText}"`;
  const response = await fetch("https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=" + GEMINI_API_KEY, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      contents: [{
        role: "user",
        parts: [{ text: prompt }]
      }]
    })
  });
  const data = await response.json();
  // Extract the text response (simple handling)
  const result = data?.candidates?.[0]?.content?.parts?.[0]?.text?.trim();
  // Normalize to Easy/Medium/Hard
  if (!result) return "Easy";
  const lowered = result.toLowerCase();
  if (lowered.includes("hard")) return "Hard";
  if (lowered.includes("medium")) return "Medium";
  return "Easy";
}
