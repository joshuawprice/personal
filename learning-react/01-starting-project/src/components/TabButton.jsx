export default function TabButton({ children, isSelected, onClick }) {
  return (
    <li>
      <button className={isSelected ? "active" : null} onClick={onClick}>
        {children}
      </button>
    </li>
  );
}
