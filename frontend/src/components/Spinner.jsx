function Spinner({ message = "Loading..." }) {

    return (

        <div
            className="
            min-h-screen
            bg-purple-100
            flex
            flex-col
            items-center
            justify-center
            gap-6
            "
        >

            <div className="relative">

                <div
                    className="
                    w-20
                    h-20
                    border-4
                    border-purple-200
                    rounded-full
                    "
                ></div>

                <div
                    className="
                    absolute
                    top-0
                    left-0
                    w-20
                    h-20
                    border-4
                    border-transparent
                    border-t-purple-700
                    rounded-full
                    animate-spin
                    "
                ></div>

            </div>

            <h2
                className="
                text-2xl
                font-bold
                text-purple-700
                "
            >
                {message}
            </h2>

            <p
                className="
                text-gray-500
                animate-pulse
                "
            >
                Please wait...
            </p>

        </div>

    );

}

export default Spinner;