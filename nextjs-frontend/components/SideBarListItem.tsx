import { useContext, useEffect } from "react";
import { AppContext } from "../context/AppContext";

interface ISidebarListItemProps {
    item: {
        title: string;
        cName: string;
    };
}

export default function SidebarListItem({ item }: ISidebarListItemProps) {
    const { option, setOption } = useContext(AppContext);

    // Add an onClick handler to update the option state
    const handleClick = () => {
        setOption(item.title);
    };

    // Use useEffect to log the option state variable when it changes
    useEffect(() => {
        console.log(option);
    }, [option]);

    return (
        <li className={item.cName}>
            <button
                type="button"
                className={option === item.title ? "sidebar-button selected" : "sidebar-button"}
                onClick={handleClick}
            >
                {item.title}
            </button>
        </li>
    );
}
