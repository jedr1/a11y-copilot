import {type ChangeEvent, type FormEvent, useReducer, useState} from "react";

type A11yLabel = "not_accessible_cluttered" | "accessible";

type A11yFormState = {
  label: A11yLabel | "";
}

type A11yFormAction =
  | { type: 'SET_FIELD', field: keyof A11yFormState, payload: A11yLabel | "" }
  | { type: 'RESET' };

const initialState: A11yFormState = {
  label: "",
};

function a11yFormReducer(state: A11yFormState, action: A11yFormAction) {
  switch (action.type) {
    case 'SET_FIELD':
      return { ...state, [action.field]: action.payload };
    case "RESET":
      return initialState;
    default:
      return state;
  }
}

function A11yCheckerPage() {
  const [a11yFormState, dispatch] = useReducer(a11yFormReducer, initialState);
  const [imgSrc, setImgSrc] = useState<string | null>(null);
  
  function handleChange(e: ChangeEvent<HTMLInputElement | HTMLSelectElement>) {
    dispatch({
      type: 'SET_FIELD',
      field: e.target.name as keyof A11yFormState,
      payload: e.target.value as A11yLabel | "",
    });
  }
  
  async function getScreenshot() {
    const url = "https://example.com";
    const res = await fetch(`http://127.0.0.1:5000/api/screenshot?url=${encodeURIComponent(url)}`);
    const blob = await res.blob();
    setImgSrc(URL.createObjectURL(blob));
  }
  
  async function saveScreenshot(e: FormEvent) {
    e.preventDefault();
    if (a11yFormState.label === "") {
      alert("Please select a label");
      return;
    }
    if (!imgSrc) return;

    const response = await fetch(imgSrc);
    const blob = await response.blob();

    const formData = new FormData();
    formData.append("label", a11yFormState.label);
    formData.append("screenshot", blob, "screenshot.png");

    try {
      const res = await fetch("http://127.0.0.1:5000/api/save_screenshot", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      if (!res.ok) {
        console.error("Error saving screenshot:", data);
        alert("Failed to save screenshot");
        return;
      }

      console.log("Screenshot saved:", data);
      alert("Screenshot saved successfully!");
      dispatch({ type: "RESET" });
      setImgSrc(null);

    } catch (err) {
      console.error("Network error:", err);
      alert("Network error while saving screenshot");
    }
  }
  
  return (
    <div>
      <button onClick={getScreenshot}>Get Screenshot</button>
      {imgSrc && <img src={imgSrc} alt="Website Screenshot" />}
      <div>
        <form onSubmit={saveScreenshot}>
          <select
            name="label"
            value={a11yFormState.label}
            onChange={handleChange}
          >
            <option value="">Select label</option>
            <option value="accessible">Accessible</option>
            <option value="not_accessible_cluttered">Not Accessible - Cluttered</option>
          </select>
          <button disabled={a11yFormState.label === "" || !imgSrc} type={"submit"}>Save Screenshot</button>
        </form>
      </div>
    </div>
  )
}

export default A11yCheckerPage;