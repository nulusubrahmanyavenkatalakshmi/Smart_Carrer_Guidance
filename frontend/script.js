document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("careerForm");

  if (form) {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();

      const skillsRaw = document.getElementById("skills").value;
      const skills = skillsRaw.split(",")
        .map(skill => skill.trim())
        .filter(skill => skill.length > 0)
        .map(skill => skill.charAt(0).toUpperCase() + skill.slice(1).toLowerCase());

      const data = {
        score10: parseFloat(document.getElementById("tenth").value),
        score12: parseFloat(document.getElementById("twelfth").value),
        ugscore: parseFloat(document.getElementById("ug").value),
        interests: document.getElementById("interests").value.trim().toLowerCase(),
        skills: skills
      };

      try {
        const res = await fetch("https://smart-carrer-guidance.onrender.com/predict", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify(data)
        });

        const json = await res.json();

        if (!res.ok) {
          throw new Error(json.error || `HTTP error! status: ${res.status}`);
        }

        const resultSection = document.getElementById("resultSection");
        const careerCard = document.getElementById("careerCard");
        careerCard.innerHTML = `<p><strong>Recommended Career:</strong> ${json.recommended_career}</p>`;
        resultSection.classList.remove("hidden");

      } catch (error) {
        console.error("Error fetching prediction:", error);
        alert(error.message || "Something went wrong. Please try again later.");
      }
    });
  }
});
