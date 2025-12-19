import React from 'react';

interface MockSelectorProps {
    onSelect: (handle: string) => void;
}

export function MockSelector({ onSelect }: MockSelectorProps) {
    return (
        <div className="flex gap-4 mb-4 justify-center">
            <button
                onClick={() => onSelect("tienda_spammer_shop")}
                className="px-4 py-2 bg-red-900/20 border border-red-500/30 text-red-200 rounded hover:bg-red-900/40 transition-colors"
            >
                Simular "El Catálogo" (Venta)
            </button>
            <button
                onClick={() => onSelect("usuario_ghost_fantasma")}
                className="px-4 py-2 bg-gray-800/50 border border-gray-600/30 text-gray-300 rounded hover:bg-gray-800 transition-colors"
            >
                Simular "El Fantasma" (Inactivo)
            </button>
            <button
                onClick={() => onSelect("sofia_leader_top")}
                className="px-4 py-2 bg-emerald-900/20 border border-emerald-500/30 text-emerald-200 rounded hover:bg-emerald-900/40 transition-colors"
            >
                Simular "El Líder" (Estratega)
            </button>
        </div>
    );
}
