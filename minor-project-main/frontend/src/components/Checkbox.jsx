export default function Checkbox() {
  return (
    <label className="flex items-center gap-2 text-sm mt-4 cursor-pointer">
      <input type="checkbox" className="accent-yellow-400" defaultChecked />
      <span className="text-gray-300">
        I agree to the <span className="text-yellow-400">Terms & Conditions</span>
      </span>
    </label>
  );
}
