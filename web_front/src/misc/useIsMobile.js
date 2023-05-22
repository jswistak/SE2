import { useState, useEffect } from "react";

export default function useIsMobile() {
    const MAX_MOBILE_WIDTH = 991;
    const [isMobile, setIsMobile] = useState(checkIsMobile());

    useEffect(() => {
        const handleWindowResize = () => {
            setIsMobile(checkIsMobile());
        };

        window.addEventListener("resize", handleWindowResize);

        return () => {
            window.removeEventListener("resize", handleWindowResize);
        };
    }, []);

    function checkIsMobile() {
        const isWindowNarrow = window.innerWidth <= MAX_MOBILE_WIDTH;
        return isWindowNarrow;
    }

    return isMobile;
}