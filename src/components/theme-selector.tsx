"use client";

import { cn } from "@/lib/utils";
import { Laptop, Moon, Sun } from "lucide-react";
import { useTheme } from "next-themes";

export default function ThemeSelector() {
  const { theme, setTheme } = useTheme();

  return (
    <div className="inline-flex w-fit items-center gap-1" role="radiogroup">
      <button
        onClick={() => setTheme("light")}
        aria-checked={theme === "light"}
        aria-label="Switch to light theme"
        className={cn(
          "p-[2px] hover:bg-accent2",
          theme === "light" && "bg-accent2",
        )}
        data-theme-switcher="true"
        role="radio"
        type="button"
      >
        <Sun size={12} />
      </button>

      <button
        onClick={() => setTheme("system")}
        aria-checked={theme === "system"}
        aria-label="Switch to system theme"
        className={cn(
          "p-[2px] hover:bg-accent2",
          theme === "system" && "bg-accent2",
        )}
        data-theme-switcher="true"
        role="radio"
        type="button"
      >
        <Laptop size={12} />
      </button>

      <button
        onClick={() => setTheme("dark")}
        aria-checked={theme === "dark"}
        aria-label="Switch to dark theme"
        className={cn(
          "p-[2px] hover:bg-accent2",
          theme === "dark" && "bg-accent2",
        )}
        data-theme-switcher="true"
        role="radio"
        type="button"
      >
        <Moon size={12} />
      </button>
    </div>
  );
}
