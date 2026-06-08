import { useState, useRef } from "react";

function UploadScreen({ onUpload }) {

    const [file, setFile] = useState(null);

    const inputRef = useRef(null);

    return (

        <div className="min-h-screen bg-purple-100 flex flex-col items-center pt-8">

            <h1 className="text-5xl font-bold mb-4">
                Upload Your File
            </h1>

            <p className="text-gray-600 text-xl mb-10">
                Drag and drop a file or click on the button below
            </p>

            <div
                className="
                w-[700px]
                h-[400px]
                bg-gray-100
                border-2
                border-dashed
                border-purple-600
                rounded-2xl
                flex
                flex-col
                justify-center
                items-center
                "
                onDragOver={(e) => e.preventDefault()}
                onDrop={(e) => {

                    e.preventDefault();

                    setFile(
                        e.dataTransfer.files[0]
                    );

                }}
            >

                <h2 className="text-4xl font-semibold mb-6">
                    Drag and drop your file here
                </h2>

                <p className="text-gray-500 text-2xl mb-6">
                    Formats: PNG, JPG, PDF, DOCX
                </p>

                <p className="font-bold text-xl mb-6">
                    OR
                </p>

                <button
                    className="
                    bg-gradient-to-r
                    from-purple-600
                    to-purple-800
                    text-white
                    text-xl
                    font-semibold
                    px-10
                    py-3
                    rounded-xl
                    shadow-lg
                    hover:scale-105
                    hover:shadow-xl
                    transition-all
                    duration-300
                    "
                    onClick={() =>
                        inputRef.current.click()
                    }
                >
                    Choose File
                </button>

                <input
                    type="file"
                    ref={inputRef}
                    className="hidden"
                    onChange={(e) =>
                        setFile(
                            e.target.files[0]
                        )
                    }
                />

                {
                    file &&
                    <p className="mt-4 text-purple-700 font-medium">
                        {file.name}
                    </p>
                }

                {
                    file &&
                    <button
                        onClick={() => {

                            console.log(
                                "File selected:",
                                file.name
                            );

                            onUpload(file);

                        }}

                        className="
                            bg-gradient-to-r
                            from-purple-600
                            to-purple-800
                            text-white
                            text-xl
                            font-semibold
                            px-10
                            py-3
                            rounded-xl
                            shadow-lg
                            hover:scale-105
                            hover:shadow-xl
                            transition-all
                            duration-300
                            "
                    >
                        Upload File
                    </button>
                }

            </div>

        </div>

    );
}

export default UploadScreen;