export default {
  async fetch(request, env, ctx) {
    const corsHeaders = {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
    };

    // 프리플라이트(OPTIONS) 요청 처리
    if (request.method === "OPTIONS") {
      return new Response(null, { headers: corsHeaders });
    }

    // POST 요청만 허용
    if (request.method !== "POST") {
      return new Response("Method not allowed", {
        status: 405,
        headers: corsHeaders,
      });
    }

    try {
      const { prompt } = await request.json();

      if (!prompt) {
        return new Response(
          JSON.stringify({ error: "prompt가 없습니다." }),
          {
            status: 400,
            headers: { "Content-Type": "application/json", ...corsHeaders },
          }
        );
      }

      // 환경변수에 등록된 Gemini API 키 사용
      const apiKey = env.GEMINI_API_KEY;

      if (!apiKey) {
        return new Response(
          JSON.stringify({ error: "서버에 API 키가 설정되어 있지 않습니다." }),
          {
            status: 500,
            headers: { "Content-Type": "application/json", ...corsHeaders },
          }
        );
      }

      const geminiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${apiKey}`;

      const geminiResponse = await fetch(geminiUrl, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          contents: [
            {
              parts: [{ text: prompt }],
            },
          ],
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

      return new Response(JSON.stringify({ result: text }), {
        headers: { "Content-Type": "application/json", ...corsHeaders },
      });
    } catch (err) {
      return new Response(
        JSON.stringify({ error: "서버 오류", detail: err.message }),
        {
          status: 500,
          headers: { "Content-Type": "application/json", ...corsHeaders },
        }
      );
    }
  },
};
