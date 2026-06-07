function AnalysisScreen({
    analysis,
    onDraftEmail,
    onDownload
}) {

    const compatibilityScore = 92;

    const metRequirements = [
        "React",
        "FastAPI",
        "AWS",
        "Tailwind CSS"
    ];

    const unmetRequirements = [
        "Azure",
        "Kubernetes"
    ];

    const pricing = {
        base: "$5,000",
        addons: "$2,000",
        total: "$7,000"
    };

    return (

        <div
            className="
            min-h-screen
            bg-purple-100
            flex
            justify-center
            items-center
            p-8
            "
        >

            <div
                className="
                bg-white
                w-full
                max-w-5xl
                p-8
                rounded-3xl
                shadow-xl
                "
            >

                <h1
                    className="
                    text-4xl
                    font-bold
                    text-purple-700
                    mb-8
                    "
                >
                    Analysis Result
                </h1>

                {/* Compatibility Score */}

                <div
                    className="
                    bg-purple-50
                    rounded-2xl
                    p-6
                    mb-8
                    text-center
                    "
                >

                    <h2
                        className="
                        text-xl
                        font-semibold
                        text-gray-700
                        "
                    >
                        Compatibility Score
                    </h2>

                    <p
                        className="
                        text-6xl
                        font-bold
                        text-purple-700
                        mt-2
                        "
                    >
                        {compatibilityScore}%
                    </p>

                </div>

                {/* Client Details */}

                <div
                    className="
                    grid
                    grid-cols-2
                    gap-4
                    mb-8
                    "
                >

                    <div>
                        <strong>Client Name:</strong>
                        {" "}
                        {analysis.clientName}
                    </div>

                    <div>
                        <strong>Industry:</strong>
                        {" "}
                        {analysis.industry}
                    </div>

                    <div>
                        <strong>Budget:</strong>
                        {" "}
                        {analysis.budget}
                    </div>

                    <div>
                        <strong>Deadline:</strong>
                        {" "}
                        {analysis.deadline}
                    </div>

                </div>

                {/* Requirements */}

                <div
                    className="
                    grid
                    grid-cols-2
                    gap-8
                    mb-8
                    "
                >

                    <div>

                        <h3
                            className="
                            text-2xl
                            font-semibold
                            text-green-600
                            mb-4
                            "
                        >
                            Met Requirements
                        </h3>

                        <div
                            className="
                            flex
                            flex-wrap
                            gap-3
                            "
                        >

                            {
                                metRequirements.map(
                                    (item) => (
                                        <span
                                            key={item}
                                            className="
                                            bg-green-100
                                            text-green-700
                                            px-4
                                            py-2
                                            rounded-full
                                            font-medium
                                            "
                                        >
                                            ✓ {item}
                                        </span>
                                    )
                                )
                            }

                        </div>

                    </div>

                    <div>

                        <h3
                            className="
                            text-2xl
                            font-semibold
                            text-red-600
                            mb-4
                            "
                        >
                            Unmet Requirements
                        </h3>

                        <div
                            className="
                            flex
                            flex-wrap
                            gap-3
                            "
                        >

                            {
                                unmetRequirements.map(
                                    (item) => (
                                        <span
                                            key={item}
                                            className="
                                            bg-red-100
                                            text-red-700
                                            px-4
                                            py-2
                                            rounded-full
                                            font-medium
                                            "
                                        >
                                            ✗ {item}
                                        </span>
                                    )
                                )
                            }

                        </div>

                    </div>

                </div>

                {/* Pricing Table */}

                <div
                    className="
                    bg-gray-50
                    rounded-2xl
                    p-6
                    mb-8
                    "
                >

                    <h3
                        className="
                        text-2xl
                        font-semibold
                        mb-4
                        "
                    >
                        Pricing Estimate
                    </h3>

                    <table
                        className="
                        w-full
                        text-left
                        "
                    >

                        <tbody>

                            <tr>
                                <td className="py-2">
                                    Base Package
                                </td>

                                <td className="py-2">
                                    {pricing.base}
                                </td>
                            </tr>

                            <tr>
                                <td className="py-2">
                                    Addons
                                </td>

                                <td className="py-2">
                                    {pricing.addons}
                                </td>
                            </tr>

                            <tr
                                className="
                                font-bold
                                text-lg
                                "
                            >
                                <td className="py-2">
                                    Total
                                </td>

                                <td className="py-2">
                                    {pricing.total}
                                </td>
                            </tr>

                        </tbody>

                    </table>

                </div>

                {/* Buttons */}

                <div
                    className="
                    flex
                    justify-end
                    gap-4
                    "
                >

                    <button
                        onClick={onDownload}
                        className="
                        bg-green-600
                        text-white
                        px-6
                        py-3
                        rounded-xl
                        hover:bg-green-700
                        transition
                        "
                    >
                        Download PDF
                    </button>

                    <button
                        onClick={onDraftEmail}
                        className="
                        bg-purple-700
                        text-white
                        px-6
                        py-3
                        rounded-xl
                        hover:bg-purple-800
                        transition
                        "
                    >
                        Draft Email
                    </button>

                </div>

            </div>

        </div>

    );
}

export default AnalysisScreen;