// 요청을 허용할 사이트 주소 (맨 끝에 / 없이)
const ALLOWED_ORIGINS = [
  "https://wjdrbxo77.mycafe24.com",
  "https://sweetrain0804-ship-it.github.io", // GitHub Pages 테스트용, 필요 없으면 삭제
];

const MAX_PROMPT_LENGTH = 2000; // 프롬프트 최대 글자 수 (안내문 포함)
const MAX_OUTPUT_TOKENS = 2048; // 답변 최대 길이
const RATE_LIMIT = 10; // IP당 허용 횟수
const RATE_WINDOW_MS = 60 * 60 * 1000; // 1시간

const hits = new Map<string, number[]>();

function isRateLimited(ip: string): boolean {
  const now = Date.now();
  if (hits.size > 5000) hits.clear();
  const recent = (hits.get(ip) ?? []).filter((t) => now - t < RATE_WINDOW_MS);
  if (recent.length >= RATE_LIMIT) {
    hits.set(ip, recent);
    return true;
  }
  recent.push(now);
  hits.set(ip, recent);
  return false;
}

Deno.serve(async (request: Request) => {
  const origin = request.headers.get("Origin") ?? "";

  if (!ALLOWED_ORIGINS.includes(origin)) {
    return new Response("Forbidden", { status: 403 });
  }

  const corsHeaders = {
    "Access-Control-Allow-Origin": origin,
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
    "Vary": "Origin",
  };

  if (request.method === "OPTIONS") {
    return new Response(null, { headers: corsHeaders });
  }

  if (request.method !== "POST") {
    return new Response("Method not allowed", {
      status: 405,
      headers: corsHeaders,
    });
  }

  const ip =
    request.headers.get("cf-connecting-ip") ??
    request.headers.get("x-forwarded-for")?.split(",")[0].trim() ??
    "unknown";

  if (isRateLimited(ip)) {
    return new Response(
      JSON.stringify({
        error: "오늘은 사용 횟수를 초과했어요. 잠시 후 다시 시도해주세요.",
      }),
      {
        status: 429,
        headers: { "Content-Type": "application/json", ...corsHeaders },
      }
    );
  }

  try {
    const { prompt } = await request.json();

    if (!prompt || typeof prompt !== "string") {
      return new Response(
        JSON.stringify({ error: "prompt가 없습니다." }),
        {
          status: 400,
          headers: { "Content-Type": "application/json", ...corsHeaders },
        }
      );
    }

    if (prompt.length > MAX_PROMPT_LENGTH) {
      return new Response(
        JSON.stringify({ error: "입력이 너무 깁니다. 재료를 줄여서 입력해주세요." }),
        {
          status: 400,
          headers: { "Content-Type": "application/json", ...corsHeaders },
        }
      );
    }

    const apiKey = Deno.env.get("GEMINI_API_KEY");

    if (!apiKey) {
      return new Response(
        JSON.stringify({ error: "서버에 API 키가 설정되어 있지 않습니다." }),
        {
          status: 500,
          headers: { "Content-Type": "application/json", ...corsHeaders },
        }
      );
    }

    const geminiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:generateContent?key=${apiKey}`;

    const geminiResponse = await fetch(geminiUrl, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        contents: [
          {
            parts: [{ text: prompt }],
          },
        ],
        generationConfig: {
          maxOutputTokens: MAX_OUTPUT_TOKENS,
        },
      }),
    });

    if (!geminiResponse.ok) {
      const errorText = await geminiResponse.text();
      return new Response(
        JSON.stringify({
          error: "Gemini API 호출 실패",
          detail: errorText,
        }),
        {
          status: geminiResponse.status,
          headers: { "Content-Type": "application/json", ...corsHeaders },
        }
      );
    }

    const data = await geminiResponse.json();

    const text =
      data?.candidates?.[0]?.content?.parts?.[0]?.text ??
      "응답을 생성하지 못했습니다.";

    return new Response(JSON.stringify({ text: text }), {
      headers: { "Content-Type": "application/json", ...corsHeaders },
    });
  } catch (err) {
    return new Response(
      JSON.stringify({ error: "서버 오류", detail: (err as Error).message }),
      {
        status: 500,
        headers: { "Content-Type": "application/json", ...corsHeaders },
      }
    );
  }
});
