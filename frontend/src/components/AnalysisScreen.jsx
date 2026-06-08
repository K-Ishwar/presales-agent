function AnalysisScreen({
    analysis,
    onDraftEmail,
    onDownload
}) {

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
                        {analysis.compatibility_score}%
                    </p>

                </div>

                {/* Client Information */}

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
                        Client Information
                    </h3>

                    <p className="mb-2">
                        <strong>Client Name:</strong>
                        {" "}
                        {analysis.client_name}
                    </p>

                    <p>
                        <strong>Recommended Tier:</strong>
                        {" "}
                        {analysis.recommended_tier}
                    </p>

                </div>

                {/* Summary */}

                <div
                    className="
                    bg-blue-50
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
                        Executive Summary
                    </h3>

                    <p>
                        {analysis.summary}
                    </p>

                </div>

                {/* Requirements Extracted */}

                <div
                    className="
                    bg-white
                    border
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
                        Requirements Extracted
                    </h3>

                    <ul
                        className="
                        list-disc
                        pl-6
                        space-y-2
                        "
                    >

                        {
                            analysis.requirements_extracted.map(
                                (item) => (
                                    <li key={item}>
                                        {item}
                                    </li>
                                )
                            )
                        }

                    </ul>

                </div>

                {/* Can Meet / Cannot Meet */}

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
                            Can Meet
                        </h3>

                        <div
                            className="
                            flex
                            flex-wrap
                            gap-3
                            "
                        >

                            {
                                analysis.can_meet.map(
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
                            Cannot Meet
                        </h3>

                        <div
                            className="
                            flex
                            flex-wrap
                            gap-3
                            "
                        >

                            {
                                analysis.cannot_meet.map(
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
                                    Base Price
                                </td>

                                <td className="py-2">
                                    ${analysis.base_price}
                                </td>
                            </tr>

                            {
                                analysis.addons.map(
                                    (addon) => (
                                        <tr key={addon.name}>
                                            <td className="py-2">
                                                {addon.name}
                                            </td>

                                            <td className="py-2">
                                                ${addon.price}
                                            </td>
                                        </tr>
                                    )
                                )
                            }

                            <tr
                                className="
                                font-bold
                                text-lg
                                border-t
                                "
                            >
                                <td className="py-2">
                                    Total Monthly Price
                                </td>

                                <td className="py-2">
                                    ${analysis.total_monthly_price}
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