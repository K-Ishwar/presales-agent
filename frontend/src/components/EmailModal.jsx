import { useState } from "react";
import { X, Copy, Check } from "lucide-react";

function EmailModal({ emailText, onClose }) {

    const [copied, setCopied] = useState(false);


    async function copyEmail() {

        await navigator.clipboard.writeText(emailText);

        setCopied(true);

        setTimeout(() => {
            setCopied(false);
        }, 2000);
    }

    return (

        <div
            onClick={onClose}
            className="
            fixed
            inset-0
            bg-black/50
            flex
            justify-center
            items-center
            z-50
            "
        >

            <div
                onClick={(e) => e.stopPropagation()}
                className="
                relative
                bg-white
                w-[700px]
                p-8
                rounded-3xl
                shadow-2xl
                "
            >

                <button
                    onClick={onClose}
                    className="
                    absolute
                    top-4
                    right-4
                    text-gray-500
                    hover:text-red-500
                    transition
                    "
                >
                    <X size={28} />
                </button>

                <h2
                    className="
                    text-3xl
                    font-bold
                    text-purple-700
                    mb-6
                    "
                >
                    Email Draft
                </h2>

                <textarea
                    value={emailText}
                    readOnly
                    className="
                    w-full
                    h-64
                    border
                    border-gray-300
                    rounded-xl
                    p-4
                    resize-none
                    focus:outline-none
                    "
                />

                <div
                    className="
                    flex
                    justify-between
                    items-center
                    mt-6
                    "
                >

                    {
                        copied
                        ?
                        <p
                            className="
                            text-green-600
                            flex
                            items-center
                            gap-2
                            "
                        >
                            <Check size={18} />
                            Copied!
                        </p>
                        :
                        <div></div>
                    }

                    <button
                        onClick={copyEmail}
                        className="
                        flex
                        items-center
                        gap-2
                        bg-purple-700
                        text-white
                        px-6
                        py-3
                        rounded-xl
                        hover:bg-purple-800
                        transition
                        "
                    >
                        <Copy size={18} />
                        Copy Email
                    </button>

                </div>

            </div>

        </div>

    );
}

export default EmailModal;